# VIE/VIA Job Offers Scraper

A Python script that monitors and notifies about new job offers from the Business France VIE/VIA platform.

## Overview

This project scrapes job offers from the Business France VIE/VIA API and sends email notifications when new offers are detected. It maintains a local cache of previously fetched data to track changes.

## Features

- Fetches job offers from the Business France API using pagination
- Tracks new job postings by comparing with previously saved data
- Sends HTML-formatted email notifications for new job offers
- Stores job data and metadata locally for future comparisons

## Project Structure

```
vie-via-scraper/
│
├── bf_api_caller.py           # Main script for fetching and processing data
├── api_data.json        # Cached job offers data
├── api_metadata.json    # Metadata about last fetch
└── requirements.txt     # Project dependencies
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure email settings in `bf_api_caller.py`:
   - Replace `sender_email` with your Gmail address
   - Replace `receiver_email` with the target email address
   - Update the Gmail app password

## Configuration

The script requires a Gmail account configured with an App Password for sending notifications. To set this up:

1. Enable 2-Step Verification in your Google Account
2. Generate an App Password:
   - Go to Google Account Settings > Security
   - Select "App Passwords"
   - Generate a new password for "Mail"
3. Use the generated password in the script

## Usage

Run the script:
```bash
python bf_api_caller.py
```

The script will:
1. Fetch all current job offers
2. Compare with previously saved data
3. Send an email notification if new offers are found
4. Save updated data and metadata locally

## Requirements

Create a `requirements.txt` file with the following dependencies:

```
requests>=2.28.0
python-dateutil>=2.8.2
```

## Data Files

### api_data.json
Contains the full list of job offers in JSON format. Each offer includes:
- Creation date
- Mission title
- Location
- Organization name
- Other offer details

### api_metadata.json
Tracks the last fetch information:
- `last_creation_date`: Timestamp of the most recent job offer
- `total_count`: Total number of offers in the last fetch

## Email Notifications

The script sends HTML-formatted emails containing:
- Table of new job offers
- Creation date
- Job title
- Location
- Company name

## Security Notes

- The Gmail app password is hardcoded in the script. Consider using environment variables or a configuration file for better security.
- API requests include headers mimicking a web browser for compatibility.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
