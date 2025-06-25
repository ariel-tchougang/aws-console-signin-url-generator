# AWS Console URL Generator

A Python script that generates AWS Console federated sign-in URLs from temporary credentials. Perfect for providing students with direct console access during hands-on labs.

![AWS Console Sign-In](aws-console-signin.png)

## Features

- Validates temporary credentials before generating URLs
- Creates federated sign-in URLs for direct AWS Console access
- Minimal dependencies and simple command-line interface
- Built for educational environments and temporary access scenarios

## Prerequisites

- Python 3.6+
- AWS temporary credentials (AccessKeyId, SecretAccessKey, SessionToken)

## Installation

### 1. Create Python Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

**Windows:**
```PowerShell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Deactivate Environment (when done)

```bash
deactivate
```

## Usage

### Option 1: Direct Credentials

```bash
python aws_console_url_generator.py <AccessKeyId> <SecretAccessKey> <SessionToken>
```

### Option 2: Assume Role (Recommended)

```bash
python assume_role_console.py <role_arn> <role_session_name> [options]
```

#### Basic Role Assumption
```bash
python assume_role_console.py arn:aws:iam::123456789012:role/StudentRole student-session-001
```

#### With External ID
```bash
python assume_role_console.py arn:aws:iam::123456789012:role/StudentRole student-session-001 --external-id MyExternalId123
```

#### With Session Policy (File)
```bash
python assume_role_console.py arn:aws:iam::123456789012:role/StudentRole student-session-001 --session-policy-file example-session-policy.json
```

#### With Session Policy (JSON String)
```bash
python assume_role_console.py arn:aws:iam::123456789012:role/StudentRole student-session-001 --session-policy-json '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:GetObject","Resource":"*"}]}'
```

#### All Parameters Combined
```bash
python assume_role_console.py arn:aws:iam::123456789012:role/StudentRole student-session-001 --external-id MyExternalId123 --session-policy-file example-session-policy.json
```

Both scripts will output a URL that provides direct access to the AWS Console:
```
AWS Console Sign-in URL:
https://signin.aws.amazon.com/federation?Action=login&Issuer=YourApp&Destination=https%3A//console.aws.amazon.com/&SigninToken=...
```

## How It Works

1. **Credential Validation**: Verifies the provided temporary credentials using AWS STS
2. **Session Creation**: Creates a session JSON with the credentials
3. **Token Generation**: Calls AWS Federation API to get a signin token
4. **URL Construction**: Builds the final console URL with the signin token

## Files

- `aws_console_url_generator.py`: Core script for generating console URLs from credentials
- `assume_role_console.py`: Script for assuming roles and generating console URLs
- `example-session-policy.json`: Example session policy for restricting permissions
- `requirements.txt`: Python dependencies

## Use Cases

- **Educational Labs**: Provide students with temporary console access via role assumption
- **Training Sessions**: Quick console access without profile configuration
- **Demonstrations**: Easy way to share temporary AWS access with restricted permissions
- **Testing**: Validate role assumptions and temporary access
- **Cross-Account Access**: Assume roles in different AWS accounts for training

## Security Notes

- Generated URLs are valid for 12 hours (AWS default)
- Only works with temporary credentials (requires SessionToken)
- No permanent credentials are stored or logged
- URLs provide the same permissions as the original credentials

## Troubleshooting

**"Invalid or expired credentials"**: Check that your temporary credentials are still valid and all three parameters are from the same STS session.

**"400 Client Error"**: Ensure credentials are properly formatted and not expired.

## Dependencies

- `requests`: HTTP library for API calls
- `boto3`: AWS SDK for credential validation

## License

This project is provided as-is for educational purposes.