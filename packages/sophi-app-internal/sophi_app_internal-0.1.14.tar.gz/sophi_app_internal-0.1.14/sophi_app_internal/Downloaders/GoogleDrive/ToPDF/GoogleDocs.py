from googleapiclient.http import MediaIoBaseDownload
import io

from sophi_app_internal.Downloaders.GoogleDrive.GoogleDriveDownloader import GoogleDriveDownloader

class GoogleDocsDownloader(GoogleDriveDownloader):
    async def download(self, file_id, chunk_size=100_000_000):
        request = self.service.files().export_media(fileId=file_id, mimeType='application/pdf')
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request, chunksize=chunk_size)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            buffer.seek(0)
            chunk = buffer.read()
            buffer.seek(0)
            buffer.truncate(0)
            yield chunk
