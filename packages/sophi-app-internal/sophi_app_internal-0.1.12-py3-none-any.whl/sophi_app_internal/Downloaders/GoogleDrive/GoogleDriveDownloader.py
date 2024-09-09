from abc import ABC, abstractmethod

from googleapiclient.discovery import build


class GoogleDriveDownloader(ABC):
    def __init__(self, service):
        self.service = service

    @abstractmethod
    async def download(self, file_id, chunk_size=100_000_000):
        pass