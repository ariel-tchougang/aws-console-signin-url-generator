#!/usr/bin/env python3
import boto3
import json
import sys
import argparse
import random
import string
from botocore.exceptions import ClientError
from aws_console_url_generator import generate_console_url

def assume_role_and_generate_url(role_arn, role_session_name, external_id=None, session_policy=None):
    """
    Assume role and generate console URL
    """
    try:
        sts_client = boto3.client('sts')
        
        # Add random suffix to session name
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        session_name_with_suffix = f"{role_session_name}-{random_suffix}"
        
        # Prepare assume role parameters
        assume_role_params = {
            'RoleArn': role_arn,
            'RoleSessionName': session_name_with_suffix
        }
        
        if external_id:
            assume_role_params['ExternalId'] = external_id
            
        if session_policy:
            assume_role_params['Policy'] = session_policy
        
        # Assume the role
        response = sts_client.assume_role(**assume_role_params)
        
        # Extract credentials
        credentials = response['Credentials']
        access_key_id = credentials['AccessKeyId']
        secret_access_key = credentials['SecretAccessKey']
        session_token = credentials['SessionToken']
        
        # Generate console URL
        console_url = generate_console_url(access_key_id, secret_access_key, session_token)
        
        return console_url
        
    except ClientError as e:
        print(f"Error assuming role: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Assume AWS role and generate console sign-in URL')
    parser.add_argument('role_arn', help='ARN of the role to assume')
    parser.add_argument('role_session_name', help='Name for the role session')
    parser.add_argument('--external-id', help='External ID for role assumption')
    parser.add_argument('--session-policy-file', help='Path to JSON file containing session policy')
    parser.add_argument('--session-policy-json', help='Session policy as JSON string')
    
    args = parser.parse_args()
    
    # Handle session policy
    session_policy = None
    if args.session_policy_file:
        try:
            with open(args.session_policy_file, 'r') as f:
                session_policy = f.read()
        except Exception as e:
            print(f"Error reading session policy file: {e}")
            sys.exit(1)
    elif args.session_policy_json:
        session_policy = args.session_policy_json
    
    # Generate console URL
    console_url = assume_role_and_generate_url(
        args.role_arn,
        args.role_session_name,
        args.external_id,
        session_policy
    )
    
    if console_url:
        print("AWS Console Sign-in URL:")
        print(console_url)
    else:
        print("Failed to generate console URL")
        sys.exit(1)

if __name__ == "__main__":
    main()