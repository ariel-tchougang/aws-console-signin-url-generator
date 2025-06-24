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

```bash
python aws_console_url_generator.py <AccessKeyId> <SecretAccessKey> <SessionToken>
```

### Example

```bash
python aws_console_url_generator.py ASIA5UTJKD365TM6NDNX 5UjufdKDkSCfW0ZH6vMRWOHZWlJVglW1ngwcxVj3 IQoJb3JpZ2luX2VjECYaCXVzLWVhc3QtMSJH...
```

The script will output a URL that provides direct access to the AWS Console:
```
AWS Console Sign-in URL:
https://signin.aws.amazon.com/federation?Action=login&Issuer=YourApp&Destination=https%3A//console.aws.amazon.com/&SigninToken=...
```

## How It Works

1. **Credential Validation**: Verifies the provided temporary credentials using AWS STS
2. **Session Creation**: Creates a session JSON with the credentials
3. **Token Generation**: Calls AWS Federation API to get a signin token
4. **URL Construction**: Builds the final console URL with the signin token

## Use Cases

- **Educational Labs**: Provide students with temporary console access
- **Training Sessions**: Quick console access without profile configuration
- **Demonstrations**: Easy way to share temporary AWS access
- **Testing**: Validate temporary credentials and access

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