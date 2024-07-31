import subprocess
import os
from time import sleep
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
slack_token = os.getenv("slack_token")
channel_id = os.getenv("channel_id")

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def run_trufflehog(output_file):
    try:
        result = subprocess.run(['trufflehog', 'filesystem', '.'], capture_output=True, text=True)
        with open(output_file, 'w') as f:
            f.write(result.stdout)
    except Exception as e:
        print(f"Error running truffleHog: {e}")

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

def upload_to_slack(file_path, channel_id, slack_token, title, comment):
    client = WebClient(token=slack_token)
    try:
        with open(file_path, 'rb') as file_content:
            response = client.files_upload_v2(
                channel=channel_id,
                file=file_content,
                title=title,
                initial_comment=comment
            )
        print(f"File uploaded successfully: {response['file']['name']}")
    except SlackApiError as e:
        if e.response['error'] == 'channel_not_found':
            print(f"Error: The specified channel '{channel_id}' was not found. Please check the channel ID and ensure the bot is invited to the channel.")
        else:
            print(f"Error uploading file: {e.response['error']}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    secretfinder_output_file = 'secretFinder_results.txt'
    trufflehog_output_file = 'truffleHog_results.txt'
    
    open(secretfinder_output_file, 'w').close()
    open(trufflehog_output_file, 'w').close()
    
    run_trufflehog(trufflehog_output_file)
    
    scan_directory(current_directory, secretfinder_output_file)
    
    upload_to_slack(trufflehog_output_file, channel_id, slack_token, "TruffleHog Results", "Here are the results from the TruffleHog scan.")

    upload_to_slack(secretfinder_output_file, channel_id, slack_token, "SecretFinder Results", "Here are the results from the SecretFinder scan.")
