import requests
import csv
from datetime import datetime
import time
import os

# Function to convert UTC time to UNIX timestamp
def utc_to_unix(utc_time):
    pattern = '%d.%m.%Y %H:%M:%S'
    return int(time.mktime(time.strptime(utc_time, pattern)))

# Function to make an API request and return JSON data
def fetch_data(account, start_date_unix, end_date_unix, auth_token):
    url = f"https://api.monobank.ua/personal/statement/{account}/{start_date_unix}/{end_date_unix}"
    headers = {"X-Token": auth_token}
    response = requests.get(url, headers=headers)
    return response.json()

# Function to process data and write to CSV
def write_to_csv(data, filename, account_type):
    with open(filename, mode='w', encoding='utf-8', newline='') as file:  # Add newline='' to avoid blank rows
        writer = csv.writer(file)
        if account_type == "Jar":
            writer.writerow(["час", "сума", "від"])
            for item in data:
                if item:  # Check if the item is not empty
                    time_str = datetime.utcfromtimestamp(item["time"]).strftime('%d.%m.%Y %H:%M:%S')
                    description = item["description"]
                    if "Від:" in description:
                        name = description.replace("Від:", "").strip().split()[0]  # Extract first name after "Від:"
                    else:
                        name = description  # Use description as is
                    writer.writerow([time_str, item["amount"]/100, name])
        elif account_type == "Card":
            writer.writerow(["час", "сума", "від"])
            for item in data:
                if item:  # Check if the item is not empty
                    time_str = datetime.utcfromtimestamp(item["time"]).strftime('%d.%m.%Y %H:%M:%S')
                    description = item["description"]
                    if "Від:" in description:
                        name = description.replace("Від:", "").strip().split()[0]  # Extract first name after "Від:"
                    else:
                        name = description  # Use description as is
                    writer.writerow([time_str, item["amount"]/100, name])

# Main function to orchestrate the flow
def main():
    # Input your data here
    start_date = "01.04.2024 00:00:00"  # Example start date in UTC
    end_date = "30.04.2024 23:59:59"    # Example end date in UTC
    auth_token = "auth_token_id" # Place your auth token here

    # Convert dates to UNIX
    start_date_unix = utc_to_unix(start_date)
    end_date_unix = utc_to_unix(end_date)

    # Extract the month and year for filename prefix
    date_prefix = datetime.strptime(start_date, '%d.%m.%Y %H:%M:%S').strftime('%m.%Y')

    # Directory to save CSV files
    save_directory = "D:/My files/python/Work&Study/uafo"

    # Account identifiers
    jar_account = "jar_account_id"
    card_account = "card_account_id"

    # Fetch data
    jar_data = fetch_data(jar_account, start_date_unix, end_date_unix, auth_token)
    card_data = fetch_data(card_account, start_date_unix, end_date_unix, auth_token)

    # Write data to CSV, adding the date prefix to filename and saving to the specified directory
    jar_filename = os.path.join(save_directory, f"{date_prefix}_jar_data.csv")
    card_filename = os.path.join(save_directory, f"{date_prefix}_card_data.csv")
    write_to_csv(jar_data, jar_filename, "Jar")
    write_to_csv(card_data, card_filename, "Card")

if __name__ == "__main__":
    main()
