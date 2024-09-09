from hashlib import md5
import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient, BlobBlock
from dotenv import load_dotenv

load_dotenv()


class UserAzureBlobStorage:
    def __init__(self, user_id: str, connection_string=None):
        self.connection_string = connection_string or os.getenv("AZURE_DEV_STORAGE_CONNECTION_STRING")
        self.user_id = user_id
        self.container_name = "sophi-app-user-" + md5(str(user_id).encode()).hexdigest()

        self.blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.connection_string,
        )

        self.container_client = self._get_or_create_container()

    def _get_or_create_container(self):
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            container_client.get_container_properties()
        except Exception:
            container_client = self.blob_service_client.create_container(self.container_name)
        return container_client

    def upload_file(self, data, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.upload_blob(data)

    def download_file(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.download_blob()

    def delete_blob(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.delete_blob()

    def delete_all_blobs(self):
        return self.container_client.delete_blobs(*self.container_client.list_blob_names())

    async def upload_chunked_blob(self, blob_name, async_chunk_generator):
        blob_client = self.container_client.get_blob_client(blob_name)
        block_list = []
        block_id = 0

        async for chunk in async_chunk_generator:
            block_id_str = str(block_id).zfill(5)
            blob_client.stage_block(block_id=block_id_str, data=chunk)
            block_list.append(BlobBlock(block_id=block_id_str))
            block_id += 1

        blob_client.commit_block_list(block_list)

    def list_blobs(self):
        return self.container_client.list_blobs()
