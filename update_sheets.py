# ===================================================================================
#  Automated Currency Data Collector (for Google Sheets)
#
#  This script connects to the Google Sheets API using your secret key file,
#  fetches 15 years of currency data, and automatically updates your
#  online spreadsheet.
# ===================================================================================

# --- Step 1: Import the necessary tools ---
# We need a few new tools to work with the Google API.
import pandas as pd
import requests
from datetime import date, timedelta, datetime
import gspread  # The main tool for talking to Google Sheets.
from google.oauth2.service_account import Credentials
import sys
import time

# --- Step 2: Set Up Your Configuration ---
# All the settings you need to change are in this one spot.

# --- IMPORTANT: Your File Names ---
# The name of your secret key file. It must be in the same folder as this script.
# Make sure this name matches your downloaded file EXACTLY.
SERVICE_ACCOUNT_FILE = 'automated-fx-dashboard-cf63ef35bc6e.json'

# The name of your Google Sheet, as it appears in your Google Drive.
GOOGLE_SHEET_URL = 'https://docs.google.com/spreadsheets/d/12btWl4piNDKqynG0LFdl7meNIfw4W9PtKfHp5ANkvCM/edit?gid=0#gid=0'

# The settings for the data we want to fetch.
START_DATE_HISTORY = "2010-01-01"
BASE_CURRENCY_TO_FETCH = "USD"
TARGET_CURRENCIES_TO_FETCH = ["INR", "EUR", "GBP", "JPY", "AUD", "CAD", "CNY"]


def connect_to_google_sheets():
    """
    This function uses your secret key file to authorize our script and
    connect to the Google Sheets API.
    """
    print("🔑 Authenticating with Google using your secret key file...")
    try:
        # These "scopes" are the permissions we are asking for.
        # We are asking for permission to manage spreadsheets and drive files.
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        print("✅ Success! Authenticated with Google.")
        return client
    except FileNotFoundError:
        print(f"❌ FATAL ERROR: The secret key file '{SERVICE_ACCOUNT_FILE}' was not found.")
        print("Please make sure the file is in the same folder as the script and the name is correct.")
        sys.exit()
    except Exception as e:
        print(f"❌ An error occurred during authentication: {e}")
        sys.exit()

def get_the_spreadsheet(client):
    """
    This function opens the specific Google Sheet we want to work with using its URL.
    """
    print(f"📄 Opening your Google Sheet by its unique URL...")
    try:
        spreadsheet = client.open_by_url(GOOGLE_SHEET_URL)
        worksheet = spreadsheet.sheet1 # Get the very first sheet in the file.
        print("✅ Successfully opened the sheet.")
        return worksheet
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ FATAL ERROR: The Google Sheet named '{GOOGLE_SHEET_NAME}' was not found.")
        print("Please make sure the name is spelled correctly and that you have shared the sheet with the service account's email address.")
        sys.exit()
    except Exception as e:
        print(f"❌ An error occurred while opening the sheet: {e}")
        sys.exit()

def get_latest_date_from_sheet(worksheet):
    """
    This function checks the 'Date' column in our sheet to find the last date
    we saved. This prevents us from downloading data we already have.
    """
    print("🔍 Checking for the last saved date in the sheet...")
    try:
        # Get all the values from the first column (the 'Date' column).
        # [1:] skips the header row.
        date_column = worksheet.col_values(1)[1:]
        if not date_column:
            # If the column is empty (besides the header), we start from the beginning.
            print("📋 Sheet is empty. Will fetch all data from the beginning.")
            return datetime.strptime(START_DATE_HISTORY, "%Y-%m-%d").date()
        else:
            # Find the most recent date.
            latest_date = datetime.strptime(max(date_column), "%Y-%m-%d").date()
            print(f"🔍 Last saved date found: {latest_date}. Will fetch data starting from the next day.")
            return latest_date + timedelta(days=1)
    except Exception as e:
        print(f"⚠️ Could not check for the last date. Will fetch all data just in case. Error: {e}")
        return datetime.strptime(START_DATE_HISTORY, "%Y-%m-%d").date()


def fetch_data_and_save(worksheet, start_date_to_fetch):
    """
    This is the main worker function. It calls the currency API, gets the data,
    cleans it up, and appends it to our Google Sheet.
    """
    today = date.today()

    if start_date_to_fetch > today:
        print("✅ Your spreadsheet is already up to date. Nothing to do.")
        return

    print(f"🌍 Starting to fetch new data from {start_date_to_fetch.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}...")
    api_url = f"https://api.frankfurter.app/{start_date_to_fetch.strftime('%Y-%m-%d')}..{today.strftime('%Y-%m-%d')}?from={BASE_CURRENCY_TO_FETCH}&to={','.join(TARGET_CURRENCIES_TO_FETCH)}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if 'rates' not in data or not data['rates']:
            print("📭 No new data was available from the API for this period.")
            return

        print("📊 Data received. Preparing it for Google Sheets...")
        df = pd.DataFrame(data['rates']).T
        df = df.reset_index().rename(columns={'index': 'Date'})
        df['Base'] = data['base']
        
        # Sort the dates to ensure they are in chronological order before saving.
        df = df.sort_values(by='Date')

        # Convert the DataFrame into a list of lists, which is the format gspread needs.
        # We also format the numbers to have 6 decimal places.
        rows_to_add = []
        for index, row in df.iterrows():
            new_row = [row['Date'], row['Base']]
            for currency in TARGET_CURRENCIES_TO_FETCH:
                if currency in row and pd.notna(row[currency]):
                    new_row.append(f"{row[currency]:.6f}")
                else:
                    new_row.append(None) # Add a blank if the currency rate is missing
            rows_to_add.append(new_row)

        print(f"✍️ Writing {len(rows_to_add)} new day(s) of data to your Google Sheet. This may take a moment...")
        # Append all our new rows to the end of the sheet.
        worksheet.append_rows(rows_to_add, value_input_option='USER_ENTERED')
        
        print("🎉 Success! Your Google Sheet is now up to date.")

    except Exception as e:
        print(f"❌ A problem occurred during the fetch or save process. Error: {e}")


# ===================================================================================
#  This is the main part of the script that runs everything in order.
# ===================================================================================
if __name__ == "__main__":
    print("--- Starting the Automated Google Sheet Updater ---")

    # Instruction 1: Install necessary libraries if they are not already.
    # We will do this manually from the command prompt.

    # Instruction 2: Connect to Google Sheets.
    g_client = connect_to_google_sheets()

    # Instruction 3: Open the specific spreadsheet we want to use.
    g_worksheet = get_the_spreadsheet(g_client)

    # Instruction 4: Find out what date we need to start getting data from.
    start_date = get_latest_date_from_sheet(g_worksheet)

    # Instruction 5: Go get the data and save it to the sheet.
    fetch_data_and_save(g_worksheet, start_date)

    print("--- Script has finished its work. ---")
