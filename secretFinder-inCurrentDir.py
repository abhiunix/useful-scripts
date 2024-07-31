import os
import subprocess
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables
load_dotenv()
slack_token = os.getenv("slack_token")
channel_id = os.getenv("channel_id")

# Change to the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def scan_file(file_path, output_file):
    try:
        result = subprocess.run(['secretFinder', '--input', file_path, '-o', 'cli'], capture_output=True, text=True)
        with open(output_file, 'a') as f:
            f.write(f"Scanning {file_path}\n")
            f.write(result.stdout)
            f.write("\n")
    except Exception as e:
        print(f"Error scanning {file_path}: {e}")

def scan_directory(directory, output_file):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            scan_file(file_path, output_file)

def upload_to_slack(file_path, channel_id, slack_token):
    client = WebClient(token=slack_token)
    try:
        
        # Open the file in binary mode for uploading
        with open(file_path, 'rb') as file_content:
            response = client.files_upload_v2(
                channel=channel_id,
                file=file_content,
                title="SecretFinder Results",
                initial_comment="Here are the results from the SecretFinder scan."
            )
        print(f"File uploaded successfully: {response['file']['name']}")
    except SlackApiError as e:
        if e.response['error'] == 'channel_not_found':
            print(f"Error: The specified channel '{channel_id}' was not found. Please check the channel ID and ensure the bot is invited to the channel.")
        else:
            print(f"Error uploading file: {e.response['error']}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    output_file = 'secretFinder_results.txt'
    # output_file = 'secretFinder_results.txt'
    
    # Clear the output file before starting the scan
    open(output_file, 'w').close()
    
    # # # Run the directory scan
    scan_directory(current_directory, output_file)
    
    # Upload the results to Slack
    upload_to_slack(output_file, channel_id, slack_token)
