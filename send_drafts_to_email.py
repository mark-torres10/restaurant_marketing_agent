import os
import json
import tempfile
import traceback

# Import the post generation logic
from write_post import generate_post

# Import the EmailManager client
from integrations.google.email_manager import EmailManager

# --- Email Configuration (matching email_manager.py example) ---
RECIPIENT_EMAILS = ["mtorres.sandbox@gmail.com", "markptorres1@gmail.com"]
SENDER_EMAIL = "mtorres.sandbox@gmail.com"  # Must match authenticated Google account
DEFAULT_TOPIC = 'Greek'

def main():
    print(f"Generating and sending drafts for a {DEFAULT_TOPIC} restaurant...")

    # Generate posts
    facebook_post = generate_post("facebook", DEFAULT_TOPIC)
    instagram_post = generate_post("instagram", DEFAULT_TOPIC)
    email_blast_content = generate_post("email_blast", DEFAULT_TOPIC)

    # Check for LLM generation errors
    llm_errors = []
    if facebook_post.startswith("ERROR_LLM_GENERATION:"):
        llm_errors.append(f"Facebook Post: {facebook_post}")
    if instagram_post.startswith("ERROR_LLM_GENERATION:"):
        llm_errors.append(f"Instagram Post: {instagram_post}")
    if email_blast_content.startswith("ERROR_LLM_GENERATION:"):
        llm_errors.append(f"Email Blast: {email_blast_content}")

    if llm_errors:
        print("\n--- LLM Generation Errors Detected ---")
        for error in llm_errors:
            print(error)
        print("Aborting email send due to LLM errors.")
        return

    # Construct email body with clear sections
    email_body = f"""
Hello Mark,

Here are the daily marketing drafts for your {DEFAULT_TOPIC} restaurant:

--- Facebook Post ---
{facebook_post}

--- Instagram Post ---
{instagram_post}

--- Email Blast Content ---
{email_blast_content}

Best regards,
Your AI Marketing Agent
"""

    email_subject = f"Daily Restaurant Marketing Drafts - {DEFAULT_TOPIC} Cuisine"

    # --- Handle Google Credentials from Environment Variables ---
    credentials_json_str = os.getenv('GOOGLE_CREDENTIALS_JSON')
    token_json_str = os.getenv('GOOGLE_TOKEN_JSON')

    if not credentials_json_str:
        print("\n--- Configuration Error ---")
        print("Error: GOOGLE_CREDENTIALS_JSON environment variable not set. Please configure it in Replit secrets.")
        return

    # Create temporary files for credentials and token
    temp_creds_file = None
    temp_token_file = None

    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f_creds:
            f_creds.write(credentials_json_str)
            temp_creds_file = f_creds.name

        # token.json might not exist on first run, so handle it gracefully
        if token_json_str:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f_token:
                f_token.write(token_json_str)
                temp_token_file = f_token.name

        # Initialize EmailManager with temporary file paths
        email_manager = EmailManager(
            credentials_path=temp_creds_file,
            token_path=temp_token_file # Pass None if token_json_str is empty
        )

        # Send the email
        print("\nAttempting to send email via Google API...")
        email_manager.send_email(
            subject=email_subject,
            message=email_body,
            recipients=RECIPIENT_EMAILS,
            sender=SENDER_EMAIL
        )
        print("Email sending process initiated. Check console for Gmail API messages.")

    except Exception as e:
        print("\n--- Google API (Email Sending) Error ---")
        print(f"An error occurred during email sending: {e}")
        print("Full Traceback:")
        traceback.print_exc()
    finally:
        # Clean up temporary files
        if temp_creds_file and os.path.exists(temp_creds_file):
            os.remove(temp_creds_file)
            # print(f"Cleaned up temporary credentials file: {temp_creds_file}") # Commented for cleaner output
        if temp_token_file and os.path.exists(temp_token_file):
            os.remove(temp_token_file)
            # print(f"Cleaned up temporary token file: {temp_token_file}") # Commented for cleaner output

if __name__ == "__main__":
    main()
