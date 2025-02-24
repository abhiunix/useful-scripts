import requests

# Define your Slack token, channel, and file path
slack_token = "xoxb-asdasd"
channel_id = "qweqwe"  # e.g., "C01234567"
file_path = "./output.txt"

# API endpoint for sending messages
url = "https://slack.com/api/chat.postMessage"

# Headers for authorization
headers = {
    "Authorization": f"Bearer {slack_token}",
    "Content-Type": "application/json"
}

# Read the markdown file
with open(file_path, "r") as file:
    file_content = file.read()

# Prepare the message payload
payload = {
    "channel": channel_id,
    "text": file_content  # This sends the content as raw text
}

# Send the message
response = requests.post(url, headers=headers, json=payload)

# Print the JSON response from Slack
print(response.json())
