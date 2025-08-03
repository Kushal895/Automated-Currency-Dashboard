Automated Currency Exchange Rate Dashboard

🔴 Live Dashboard

This project is a fully automated, 8-page interactive dashboard that tracks the daily exchange rate of the USD against seven major world currencies.

Main Page (Summary & Navigation Hub)

<img width="1329" height="743" alt="Image" src="https://github.com/user-attachments/assets/33bf46cd-2481-430f-b1dc-9314dbb769e0" />

Detail Page (In-Depth Analysis for a Selected Currency)

<img width="1311" height="732" alt="Image" src="https://github.com/user-attachments/assets/9d9ae9e9-0f8c-49ac-ab7f-af5ca8b7a700" />

<img width="1306" height="732" alt="Image" src="https://github.com/user-attachments/assets/25cfa8af-f5af-4566-ade5-24516f8911e0" />

<img width="1310" height="722" alt="Image" src="https://github.com/user-attachments/assets/a1d4842c-8834-484a-aad6-9d4e3716518d" />

🎯 Project Objective

The goal of this project was to design and build a professional, end-to-end business intelligence pipeline. The system automatically fetches daily and historical currency exchange rate data, processes and stores it in a cloud-based data store, and visualizes the insights through a dynamic and interactive Power BI dashboard. The entire workflow is 100% automated, requiring no manual intervention.

🧰 Tech Stack & Architecture

This project utilizes a modern, serverless architecture to create a robust and scalable data pipeline.

TechnologyRolePythonThe core engine for automation, data fetching, and processing.Pandas LibraryUsed for cleaning, transforming, and structuring the raw API data.Requests LibraryUsed to perform HTTP requests to the financial data API.Google Cloud PlatformProvided the essential APIs for cloud integration.Google Sheets & Drive APIsUsed by the Python script to programmatically update the cloud data store.Google SheetsActed as a reliable, serverless cloud database for the project's data.Power BIThe business intelligence tool used for data modeling, analysis, and visualization.DAXUsed extensively within Power BI to create complex calculated measures like Moving Averages, Volatility, and Dynamic Summaries.Git & GitHubUsed for version control and professional project showcasing.

Export to Sheets

🔄 Automation Workflow

The system is automated in two stages:



Backend (Python): A Python script (update_sheets.py) is scheduled to run daily via Windows Task Scheduler. It fetches the latest rates from the Frankfurter API and appends them to the Google Sheet.

Frontend (Power BI): The published Power BI report is configured with a Scheduled Refresh in the Power BI Service. It automatically pulls the new data from the Google Sheet each day, ensuring the dashboard is always up-to-date.

✨ Key Features

End-to-End Automation: No manual steps are required to update the data or the dashboard.

Interactive Navigation: The Main Page acts as a hub. Clicking on any currency card seamlessly navigates the user to a dedicated detail page for that currency using Power BI's bookmarking feature.

Rich Data Visualization: The dashboard includes a variety of visuals to provide deep insights:

KPI Cards for latest rate, all-time high/low, and daily % change.

Historical Trend Chart with 7-day and 30-day moving averages to identify trends.

Recent Volatility Chart showing daily performance over the last 60 days.

Dynamic Text Summaries: A natural-language summary on each detail page is generated automatically using DAX, explaining the currency's current performance and historical context.

Cloud-Based Architecture: Leverages Google Cloud APIs and Google Sheets as a data store, demonstrating modern, serverless data engineering practices.
