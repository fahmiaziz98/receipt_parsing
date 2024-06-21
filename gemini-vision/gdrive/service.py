import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import logging
import json

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

class GoogleDriveService:

    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self):
        base_path = "/home/fahmiaziz/project_py/gcp"
        credential_path = os.path.join(base_path, "service-account.json")
        
        if not os.path.exists(credential_path):
            logging.error("Google Drive connection credentials are not found! They need to be stored here {}".format(credential_path))
        else:
            logging.info("Found credentials file: {}".format(credential_path))
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

    def build(self):
        credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        logging.info("Loading credentials from: {}".format(credential_path))
        
        try:
            with open(credential_path, 'r') as f:
                credentials_data = json.load(f)
        except Exception as e:
            logging.error("Failed to load credentials file: {}".format(e))
            raise
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credential_path, self.SCOPES
        )
        
        service = build("drive", "v3", credentials=creds, cache_discovery=False)
        return service

# if __name__ == "__main__":
#     gdrive_service = GoogleDriveService()
#     try:
#         service = gdrive_service.build()
#         logging.info("Google Drive service created successfully.")
#     except Exception as e:
#         logging.error("Failed to create Google Drive service: {}".format(e))
