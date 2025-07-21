import boto3
import json

def get_secret():
    client = boto3.client("secretsmanager", region_name="ap-south-1")
    response = client.get_secret_value(SecretId="slack-security-webhooks")
    secret = response.get("SecretString")

    if not secret:
        import base64
        secret = base64.b64decode(response["SecretBinary"]).decode("utf-8")

    secret_dict = json.loads(secret)
    for k, v in secret_dict.items():
        print(f"{k}: {v}")

    return secret_dict

if __name__ == "__main__":
    get_secret()
