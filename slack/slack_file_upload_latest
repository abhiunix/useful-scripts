#!/usr/bin/env python3
"""
Simple script to upload a file to Slack using the new API.
Usage: python slack_upload.py <file_path>
"""

import sys
import requests
import os
from dotenv import load_dotenv

def get_channel_id(token, channel):
    """
    Convert channel name to channel ID if needed.
    
    Args:
        token: Slack Bot Token
        channel: Channel name (without #) or channel ID
    
    Returns:
        Channel ID or None if not found
    """
    # If it's already a channel ID (starts with C), return it
    if channel.startswith('C'):
        return channel
    
    # Otherwise, look up the channel by name
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"types": "public_channel,private_channel"}
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    
    if not result.get('ok'):
        print(f"✗ Failed to list channels: {result.get('error')}")
        return None
    
    # Search for the channel by name
    channel_name = channel.lstrip('#')
    for ch in result.get('channels', []):
        if ch['name'] == channel_name:
            return ch['id']
    
    print(f"✗ Channel '{channel}' not found")
    return None

def upload_file_to_slack(file_path, token, channel):
    """
    Upload a file to Slack channel using the new API methods.
    
    Args:
        file_path: Path to the file to upload
        token: Slack Bot Token (xoxb-...)
        channel: Channel ID or name to upload to
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        return False
    
    # Get channel ID if channel name was provided
    channel_id = get_channel_id(token, channel)
    if not channel_id:
        return False
    
    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    # Step 1: Get upload URL
    print(f"📤 Preparing to upload: {filename}")
    
    get_url_endpoint = "https://slack.com/api/files.getUploadURLExternal"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "filename": filename,
        "length": file_size
    }
    
    response = requests.post(get_url_endpoint, headers=headers, data=data)
    result = response.json()
    
    if not result.get('ok'):
        print(f"✗ Failed to get upload URL: {result.get('error')}")
        return False
    
    upload_url = result['upload_url']
    file_id = result['file_id']
    
    # Step 2: Upload file to the URL
    print(f"⬆️  Uploading file...")
    
    with open(file_path, 'rb') as file:
        upload_response = requests.post(
            upload_url,
            files={'file': file}
        )
    
    if upload_response.status_code != 200:
        print(f"✗ File upload failed with status: {upload_response.status_code}")
        return False
    
    # Step 3: Complete the upload
    print(f"✅ Finalizing upload...")
    
    complete_endpoint = "https://slack.com/api/files.completeUploadExternal"
    
    # Convert files array to JSON string for form data
    import json
    complete_data = {
        "files": json.dumps([{"id": file_id, "title": filename}]),
        "channel_id": channel_id
    }
    
    complete_response = requests.post(
        complete_endpoint,
        headers=headers,
        data=complete_data  # Send as form data, not JSON
    )
    
    complete_result = complete_response.json()
    
    if complete_result.get('ok'):
        print(f"✓ File uploaded successfully: {filename}")
        return True
    else:
        print(f"✗ Upload completion failed: {complete_result.get('error')}")
        return False

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python slack_upload.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Get credentials from environment variables
    SLACK_TOKEN = os.getenv("SLACK_TOKEN")
    CHANNEL = os.getenv("SLACK_CHANNEL")
    
    # Validate credentials
    if not SLACK_TOKEN:
        print("Error: SLACK_TOKEN not found in .env file")
        sys.exit(1)
    if not CHANNEL:
        print("Error: SLACK_CHANNEL not found in .env file")
        sys.exit(1)
    
    # Upload the file
    upload_file_to_slack(file_path, SLACK_TOKEN, CHANNEL)

if __name__ == "__main__":
    main()
