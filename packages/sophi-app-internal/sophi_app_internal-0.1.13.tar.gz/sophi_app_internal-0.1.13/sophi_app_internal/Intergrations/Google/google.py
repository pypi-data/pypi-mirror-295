import io
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

from sophi_app_internal.Downloaders.GoogleDrive.ToPDF.GoogleDocs import GoogleDocsDownloader
from sophi_app_internal.Downloaders.GoogleDrive.ToPDF.GoogleDrivePDF import PDFDownloader
from sophi_app_internal.Downloaders.GoogleDrive.ToXLSX.GoogleSpreadsheet import GoogleSpreadsheetDownloader

load_dotenv()
class UserGoogleDrive:
    def __init__(self, user):
        self.user = user
        user_identities = user['identities']
        google_identity = [identity for identity in user_identities if identity['provider'] == 'google-oauth2'][0]

        access_token = google_identity['access_token']
        refresh_token = google_identity['refresh_token']

        creds = Credentials.from_authorized_user_info({
            "token": access_token,
            "refresh_token": refresh_token,
            "client_id": os.getenv('GOOGLE_CLIENT_ID'),
            "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
        })

        self.access_token = creds.token
        self.refresh_token = creds.refresh_token

        self.service = build('drive', 'v3', credentials=creds)

    def list_files_in_folder(self, folder_id):
        all_files = []
        query = f"'{folder_id}' in parents and trashed = false"
        page_token = None

        while True:
            results = self.service.files().list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token
            ).execute()
            items = results.get('files', [])

            for item in items:
                if item['mimeType'] != 'application/vnd.google-apps.folder':
                    all_files.append(item)
                else:
                    all_files.extend(self.list_files_in_folder(item['id']))

            page_token = results.get('nextPageToken')
            if not page_token:
                break

        return all_files

    def retrieve_google_drive_files_for_folder(self, folder_ids):
        all_files = []
        for folder_id in folder_ids:
            all_files.extend(self.list_files_in_folder(folder_id))
        return all_files

    def retrieve_google_drive_files(self, file_ids):
        files = []
        for file_id in file_ids:
            file = self.service.files().get(fileId=file_id).execute()
            files.append(file)

        return files

    def retrieve_folder_id_by_name(self, service, folder_name):
        response = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive',
            fields='files(id, name)'
        ).execute()

        folders = response.get('files', [])
        if not folders:
            raise Exception(f"Folder '{folder_name}' not found.")

        return folders[0]['id']

    async def download_file(self, file, chunk_size=100_000_000):
        file_id = file['id']
        downloader = self.get_downloader(file)(self.service)

        async for chunk in downloader.download(file_id, chunk_size):
            yield chunk

    def get_downloader(self, file):
        mime_type = file['mimeType']
        downloader_map = {
            'application/vnd.google-apps.document': GoogleDocsDownloader,
            'application/vnd.google-apps.presentation': GoogleDocsDownloader,
            'application/vnd.google-apps.drawing': GoogleDocsDownloader,
            'application/pdf': PDFDownloader,
            'application/vnd.google-apps.spreadsheet': GoogleSpreadsheetDownloader
        }

        try:
            return downloader_map[mime_type]
        except KeyError:
            raise Exception(f"No downloader found for mimeType: {mime_type}")

    def get_file_name_extension(self, file):
        mime_type = file['mimeType']

        # we map the external mime type to our internal accepted file extensions
        extension_map = {
            'application/vnd.google-apps.document': 'pdf',
            'application/vnd.google-apps.presentation': 'pdf',
            'application/vnd.google-apps.drawing': 'pdf',
            'application/pdf': 'pdf',
            'application/vnd.google-apps.spreadsheet': 'xlsx'
        }

        try:
            return extension_map[mime_type]
        except KeyError:
            raise Exception(f"No extension found for mimeType: {mime_type}")