# Plan for `send_drafts_to_email.py`

This document outlines the step-by-step plan to create a Python script (`send_drafts_to_email.py`) that generates marketing posts for a Greek restaurant and sends them to a specified email address (`markptorres1@gmail.com`) using Google's Gmail API for authentication.

## 1. Identify Email Sending Library

We will use Python's built-in `smtplib` and `email.mime.text` modules for sending emails, as they provide direct control and are commonly used for SMTP communication. For Google authentication, we will leverage `google-auth-oauthlib` and `google-auth-httplib2` to handle the OAuth 2.0 flow.

## 2. Google Authentication Setup (User Action Required)

To send emails via Gmail API, OAuth 2.0 authentication is required. This involves setting up a Google Cloud Project and obtaining credentials. **The user will need to perform these steps in their Google Cloud Console:**

*   **Create a Google Cloud Project:** If you don't have one, create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
*   **Enable Gmail API:** Navigate to "APIs & Services" > "Library" and search for "Gmail API". Enable it for your project.
*   **Create OAuth 2.0 Client ID:**
    *   Go to "APIs & Services" > "Credentials".
    *   Click "+ Create Credentials" and select "OAuth client ID".
    *   Choose "Desktop app" as the application type. Give it a descriptive name (e.g., "Restaurant Marketing Agent").
    *   Click "Create".
    *   **Download `credentials.json`:** After creation, you will be presented with your client ID and client secret. Click the "Download JSON" button to save `credentials.json` to your local machine. **DO NOT UPLOAD THIS FILE DIRECTLY TO REPLIT OR COMMIT TO GIT.**
*   **Consent Screen Configuration:** Ensure your OAuth consent screen is configured. For personal use, you can set it to "External" and "Testing" status. Add `markptorres1@gmail.com` as a test user.

## 3. Securely Handling Google Credentials in Replit

Since `credentials.json` and `token.json` contain sensitive information, we will use Replit's Secrets feature to store them securely.

*   **Storing `credentials.json`:**
    1.  Open the `credentials.json` file you downloaded with a text editor.
    2.  Copy its entire content.
    3.  In your Replit workspace, go to the "Secrets" tab (lock icon).
    4.  Add a new secret:
        *   **Key:** `GOOGLE_CREDENTIALS_JSON`
        *   **Value:** Paste the entire content of your `credentials.json` file here.
*   **Storing `token.json` (for subsequent runs):**
    1.  The first time you run `send_drafts_to_email.py` locally (or in a temporary Repl), it will prompt you to authorize and then generate a `token.json` file. This file contains the refresh token needed for subsequent non-interactive authentications.
    2.  Once `token.json` is generated, open it with a text editor and copy its entire content.
    3.  In your Replit workspace, go to the "Secrets" tab.
    4.  Add a new secret:
        *   **Key:** `GOOGLE_TOKEN_JSON`
        *   **Value:** Paste the entire content of your `token.json` file here.
*   **Modifying `send_drafts_to_email.py`:** The script will be modified to read the content of `credentials.json` and `token.json` from these environment variables instead of directly from files.

## 4. Integrate Post Generation

*   The `send_drafts_to_email.py` script will import the `generate_post` function from the existing `write_post.py` file.
*   It will call `generate_post` three times, once for each platform (Facebook, Instagram, Email Blast), using "Greek" as the default topic.

## 5. Construct Email Content

*   The generated Facebook, Instagram, and Email Blast posts will be combined into a single, well-formatted email body.
*   A clear and informative subject line will be created for the email (e.g., "Daily Restaurant Marketing Drafts - Greek Cuisine").

## 6. Implement Email Sending Logic

*   The script will use `google-auth-oauthlib.flow` to handle the OAuth 2.0 authorization flow. It will attempt to load credentials from `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON` environment variables.
*   It will then use `smtplib` to connect to `smtp.gmail.com` on port 587 (TLS).
*   Authentication will be performed using the OAuth 2.0 access token obtained from the credentials.
*   The `email.mime.text.MIMEText` class will be used to create the email message.
*   The email will be sent to `markptorres1@gmail.com`.

## 7. Error Handling

*   Appropriate `try-except` blocks will be implemented to handle potential errors during post generation (e.g., OpenAI API issues) and email sending (e.g., authentication failures, network issues).

## 8. Update Dependencies

*   The `requirements.txt` file will be updated to include `google-auth-oauthlib` and `google-auth-httplib2`.

## 9. Replit Cron Job Configuration

To run `send_drafts_to_email.py` as a scheduled task in Replit:

1.  **Enable Always On (if available):** For Repls that need to run scheduled tasks, enabling "Always On" (a Replit Hacker plan feature) can ensure your Repl is always ready.
2.  **Set up a Scheduled Repl:**
    *   In your Replit workspace, go to the "Tools" section (often a hammer icon or similar).
    *   Look for "Scheduled Repls" or "Cron Jobs".
    *   Click to add a new schedule.
    *   **Command:** Enter the command to run your script. For example:
        ```bash
        python send_drafts_to_email.py
        ```
    *   **Schedule:** Configure the frequency (e.g., daily, every two days) according to your needs.
    *   **Environment Variables:** Ensure that the `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON` secrets you set up in step 3 are available to the scheduled task. Replit usually makes all secrets available to scheduled tasks automatically.

This setup ensures that your email sending script runs automatically and securely on Replit.