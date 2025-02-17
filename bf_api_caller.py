import json
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def fetch_data_with_curl(skip, limit):
    curl_command = [
        "curl",
        "https://civiweb-api-prd.azurewebsites.net/api/Offers/search",
        "-H", "Accept: */*",
        "-H", "Accept-Language: fr-FR,fr;q=0.9",
        "-H", "Connection: keep-alive",
        "-H", "Content-Type: application/json",
        "-H", "Origin: https://mon-vie-via.businessfrance.fr",
        "-H", "Referer: https://mon-vie-via.businessfrance.fr/",
        "-H", "Sec-Fetch-Dest: empty",
        "-H", "Sec-Fetch-Mode: cors",
        "-H", "Sec-Fetch-Site: cross-site",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "-H", "sec-ch-ua: \"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "-H", "sec-ch-ua-mobile: ?0",
        "-H", "sec-ch-ua-platform: \"Windows\"",
        "--data-raw",
        json.dumps({
            "limit": limit,
            "skip": skip,
            "sort": ["0"],
            "activitySectorId": [],
            "missionsTypesIds": [],
            "missionsDurations": [],
            "gerographicZones": [],
            "countriesIds": [],
            "studiesLevelId": [],
            "companiesSizes": [],
            "specializationsIds": [],
            "entreprisesIds": [0],
            "missionStartDate": None,
            "query": None
        })
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True, encoding='utf-8')
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        print(f"Failed to fetch data: {result.stderr}")
        return None

all_data = []
limit = 100
skip = 0
total_count = None

# Fetch data in batches
while True:
    data = fetch_data_with_curl(skip, limit)
    if not data:
        break

    results = data.get('result', [])
    if not results:
        break

    all_data.extend(results)
    skip += limit
    total_count = data.get('count', 0)

    if skip >= total_count:
        break

last_creation_date = max(item.get('creationDate') for item in all_data) if all_data else None

# Load previously saved metadata
try:
    with open('api_metadata.json', 'r') as f:
        metadata = json.load(f)
        previous_last_creation_date = metadata.get('last_creation_date')
        previous_total_count = metadata.get('total_count')
except FileNotFoundError:
    previous_last_creation_date = None
    previous_total_count = 0

# Detect new items
new_items = []
if total_count > previous_total_count or (last_creation_date and last_creation_date > previous_last_creation_date):
    for item in all_data:
        creation_date = item.get('creationDate')
        if creation_date and creation_date > previous_last_creation_date:
            new_items.append(item)

# Send email notification if new items are detected
if new_items:
    sender_email = "[SENDER_MAIL]"  # Replace with your email
    receiver_email = "[RECIPIENT_MAIL]"  # Replace with the recipient's email
    subject = "New Offers Detected"

    # Beautiful mail content using HTML
    body = """
    <html>
    <head>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h2>New Offers Detected</h2>
        <table>
            <tr>
                <th>Date</th>
                <th>Job Title</th>
                <th>Location</th>
                <th>Company</th>
            </tr>
    """

    for item in new_items:
        creation_date = item.get('creationDate')
        job_title = item.get('missionTitle')
        location = item.get('cityName')
        company_name = item.get('organizationName')
        body += f"""
            <tr>
                <td>{creation_date}</td>
                <td>{job_title}</td>
                <td>{location}</td>
                <td>{company_name}</td>
            </tr>
        """

    body += """
        </table>
    </body>
    </html>
    """

    # Set up the SMTP server
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, "[PASSWORD_SENDER_MAIL]")  # Replace with your email password
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

# Save the last creation date and total count to a file
with open('api_data.json', 'w') as f:
    json.dump(all_data, f, indent=4)

with open('api_metadata.json', 'w') as f:
    json.dump({'last_creation_date': last_creation_date, 'total_count': total_count}, f, indent=4)

print("Data fetching complete. Metadata saved.")
