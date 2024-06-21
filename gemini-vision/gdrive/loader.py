import io
import os
import logging
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import googleapiclient.discovery
from typing import List

from service import GoogleDriveService

# Configure logging
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

class GoogleDriveLoader:
    VALID_EXTENSIONS = [".pdf", ".png", ".jpeg"]

    def __init__(self, service: googleapiclient.discovery.Resource, folder_id: str):
        self.service = service
        self.folder_id = folder_id

    def search_for_files(self) -> List:
        """
        See https://developers.google.com/drive/api/guides/search-files#python
        """
        query = f"'{self.folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and ("
        for i, ext in enumerate(self.VALID_EXTENSIONS):
            if i == 0:
                query += f"name contains '{ext}' "
            else:
                query += f"or name contains '{ext}' "
        query = query.rstrip()
        query += ")"

        logging.info("Searching for files with query: %s", query)

        # create drive api client
        files = []
        page_token = None
        try:
            while True:
                response = (
                    self.service.files()
                    .list(
                        q=query,
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                for file in response.get("files"):
                    logging.info(f'Found file: {file.get("name")}, {file.get("id")}')
                    file_id = file.get("id")
                    file_name = file.get("name")

                    files.append(
                        {
                            "id": file_id,
                            "name": file_name,
                        }
                    )

                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    break

        except HttpError as error:
            logging.error(f"An error occurred during file search: {error}")
            files = None

        if not files:
            logging.info("No files found matching the search criteria.")

        return files

    def download_file(self, real_file_id: str, save_path: str) -> bool:
        """
        Downloads a file and saves it to the specified path
        """
        logging.info("Starting download for file ID: %s", real_file_id)

        try:
            file_id = real_file_id
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                logging.info(f"Download progress: {int(status.progress() * 100)}%.")

            # Save the downloaded content to a file
            with open(save_path, 'wb') as f:
                f.write(file.getvalue())
            logging.info(f"File saved to {save_path}")
            return True

        except HttpError as error:
            logging.error(f"An error occurred during file download: {error}")
            return False

# # Example usage
# if __name__ == "__main__":
#     # Replace 'service' with the actual Google Drive service object you created
#     service = GoogleDriveService().build()
#     folder_id = "1BGLZEK8R5am0tM40nXD5-MK5ZGy-WXRd"  # Replace with the actual folder ID of the "receiptchat" folder
#     gdrive_loader = GoogleDriveLoader(service, folder_id)

#     files = gdrive_loader.search_for_files()
#     if files:
#         download_folder = "/home/fahmiaziz/project_py/receipt_parsing/gemini-vision"  # Replace with the actual path where you want to save the files
#         os.makedirs(download_folder, exist_ok=True)

#         for file in files:
#             logging.info(f"Attempting to download file: {file['name']} ({file['id']})")
#             save_path = os.path.join(download_folder, file['name'])
#             success = gdrive_loader.download_file(file['id'], save_path)
#             if success:
#                 logging.info(f"Successfully downloaded and saved file: {file['name']} to {save_path}")
#             else:
#                 logging.warning(f"Failed to download file: {file['name']}")
#     else:
#         logging.info("No files found to download.")
