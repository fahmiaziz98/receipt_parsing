import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import logging

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

class GoogleDriveService:

    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self):
        # the directory where your credentials are stored
        base_path = "/home/fahmiaziz/project_py/gcp"
        
        # The name of the file containing your credentials
        credential_path = os.path.join(base_path, "gdrive.json")
        if not os.path.exists(credential_path):
            logging.error(
                "Google Drive connection credentials are not found! They need to be stored here {}".format(
                    credential_path
                )
            )
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

    def build(self):
        
        # Get credentials into the desired format
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), self.SCOPES
        )  
        
        # Set up the Gdrive service object
        service = build("drive", "v3", credentials=creds, cache_discovery=False)

        return service