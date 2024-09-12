import asyncio
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from worker_automate_hub.utils.env import CREDENTIALS
from worker_automate_hub.api.client import get_config_by_name


def get_token_gcp():
    get_gcp_token = asyncio.run(get_config_by_name("GCP_SERVICE_ACCOUNT"))
    get_gcp_credentials = asyncio.run(get_config_by_name("GCP_CREDENTIALS"))
    return get_gcp_token, get_gcp_credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://mail.google.com/",
]


class GetCredsGworkspace:
    def get_creds_gworkspace(self):
        creds = None
        gcp_token, gcp_credentials = get_token_gcp()

        try:
            creds = Credentials.from_authorized_user_file(
                gcp_token,
                SCOPES,
            )

        except Exception as e:
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        gcp_credentials,
                        SCOPES,
                    )

                    creds = flow.run_local_server(port=0)
                with open(
                    gcp_token,
                    "w",
                ) as token:

                    token.write(creds.to_json())

        return creds