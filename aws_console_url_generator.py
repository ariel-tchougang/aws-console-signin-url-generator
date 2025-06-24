#!/usr/bin/env python3
import json
import urllib.parse
import requests
import sys
import boto3
from botocore.exceptions import ClientError

def validate_credentials(access_key_id, secret_access_key, session_token):
    """Test if credentials are valid"""
    try:
        client = boto3.client(
            'sts',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token
        )
        client.get_caller_identity()
        return True
    except ClientError:
        return False

def generate_console_url(access_key_id, secret_access_key, session_token):
    """
    Generate AWS Console federated sign-in URL from temporary credentials
    """
    # Validate credentials first
    if not validate_credentials(access_key_id, secret_access_key, session_token):
        print("Error: Invalid or expired credentials")
        return None
    # Step 1: Create the session string
    session_json = {
        "sessionId": access_key_id,
        "sessionKey": secret_access_key,
        "sessionToken": session_token
    }
    
    # Step 2: Make request to federation endpoint
    federation_url = "https://signin.aws.amazon.com/federation"
    
    try:
        response = requests.get(federation_url, params={
            "Action": "getSigninToken",
            "Session": json.dumps(session_json, separators=(',', ':'))
        })
        response.raise_for_status()
        signin_token = response.json()["SigninToken"]
    except Exception as e:
        print(f"Error getting signin token: {e}")
        return None
    
    # Step 4: Create the final console URL
    console_url = (
        f"https://signin.aws.amazon.com/federation"
        f"?Action=login"
        f"&Issuer=YourApp"
        f"&Destination={urllib.parse.quote_plus('https://console.aws.amazon.com/')}"
        f"&SigninToken={signin_token}"
    )
    
    return console_url

def main():
    if len(sys.argv) != 4:
        print("Usage: python aws_console_url_generator.py <AccessKeyId> <SecretAccessKey> <SessionToken>")
        sys.exit(1)
    
    access_key_id = sys.argv[1]
    secret_access_key = sys.argv[2]
    session_token = sys.argv[3]
    
    console_url = generate_console_url(access_key_id, secret_access_key, session_token)
    
    if console_url:
        print("AWS Console Sign-in URL:")
        print(console_url)
    else:
        print("Failed to generate console URL")
        sys.exit(1)

if __name__ == "__main__":
    main()