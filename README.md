# Gmail Inbox Manager

I do not like unread emails in my gmail.

## How to run

1. Set up Google Cloud Project and get credentials:

   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing one
   - Enable the Gmail API for your project
   - Go to "Credentials" section
   - Click "Create Credentials" and select "OAuth client ID"
   - Choose "Desktop Application" as application type
   - Download the credentials and save as `credentials.json` in project root

   The `credentials.json` file should contain the following fields:

   - `client_id`: Your OAuth 2.0 client ID (ends with .apps.googleusercontent.com)
   - `project_id`: Your Google Cloud project ID
   - `auth_uri`: OAuth 2.0 authorization endpoint
   - `token_uri`: OAuth 2.0 token endpoint
   - `auth_provider_x509_cert_url`: Certificate URL
   - `client_secret`: Your client secret (keep this secure!)
   - `redirect_uris`: Authorized redirect URIs (usually http://localhost)

   A sample structure is provided in `sample-credentials.json`.

2. Set up Python environment:

   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   
   # Install requirements
   pip install -r requirements.txt
   ```

3. Run the script:

   ```bash
   python app.py
   ```

## Authentication

The first time you run the script, it will:

1. Open your default web browser
2. Ask you to sign in to your Google account
3. Request permission to access your Gmail
4. Create a `token.json` file to store your authentication credentials

The `token.json` file allows the script to run without re-authentication in future executions.

## Troubleshooting

Common issues and solutions:

1. Permission Errors

   - If you get permission errors after changing scopes or credentials
   - Delete `token.json` and run the script again
   - This will trigger a fresh authentication flow

2. Authentication Failed

   - Check if your `credentials.json` is properly configured
   - Ensure Gmail API is enabled in your Google Cloud Console
   - Try deleting both `token.json` and `credentials.json`
   - Download fresh credentials and authenticate again

3. Scope Issues

   - If you see "insufficient permission" errors
   - Delete `token.json` and re-run the script
   - This will prompt for consent with the updated scopes
