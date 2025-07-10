import os.path
from typing import Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Unified scopes for all Google integrations (Gmail send + Calendar events)
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar.events"
]

class GoogleAPICore:
    """
    Base class for Google API integrations. Handles OAuth2 credential loading, token refresh,
    and service building for Google APIs.
    """
    def __init__(
        self,
        api_name: str,
        api_version: str,
        scopes: Optional[list[str]] = None,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
    ):
        self.api_name = api_name
        self.api_version = api_version
        self.scopes = scopes or SCOPES
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.credentials_path = credentials_path or os.path.join(self.current_dir, "credentials.json")
        self.token_path = token_path or os.path.join(self.current_dir, "token.json")
        self.service = self._get_service()

    def _get_service(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Try to load credentials from environment variables first
                client_id = os.environ.get("GOOGLE_CLIENT_ID")
                client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
                refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN")

                if client_id and client_secret and refresh_token:
                    creds = Credentials(
                        None,
                        refresh_token=refresh_token,
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id=client_id,
                        client_secret=client_secret,
                        scopes=self.scopes,
                    )
                    # Refresh the credentials to get a new access token
                    creds.refresh(Request())
                else:
                    # Fallback to local flow if no environment variables are set
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.scopes
                    )
                    creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return build(self.api_name, self.api_version, credentials=creds)

