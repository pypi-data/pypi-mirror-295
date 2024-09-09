import os
import logging
from azure.cosmos import CosmosClient, exceptions
from typing import List, Dict, Optional

class CosmosContainerClient:
    _client_instance = None

    def __new__(cls, *args, **kwargs):
        if cls._client_instance is None:
            cls._client_instance = super(CosmosContainerClient, cls).__new__(cls)
        return cls._client_instance

    def __init__(self, connection_string: str, db_name: str, container_name: str):
        if not hasattr(self, 'initialized'):
            self.account_client = CosmosClient.from_connection_string(connection_string)
            self.db_client = self.account_client.get_database_client(db_name)
            self.container_client = self.db_client.get_container_client(container_name)
            self.initialized = True

    def set_database_and_container(self, db_name: str, container_name: str):
        """
        Set the database and container client to a different database and container.

        :param db_name: Name of the database to switch to.
        :param container_name: Name of the container to switch to.
        """
        self.db_client = self.account_client.get_database_client(db_name)
        self.container_client = self.db_client.get_container_client(container_name)

    def query_cosmosdb_container(
        self,
        query: str,
        partition_key: Optional[List[str]] = None,
        parameters: Optional[List[Dict[str, str]]] = None,
        enable_cross_partition_query: Optional[bool] = None
    ):
        """
        Query items in the Cosmos DB container.

        :param query: SQL query string.
        :param partition_key: Optional list of partition key strings.
        :param parameters: Optional list of dictionaries containing query parameters.
        :param enable_cross_partition_query: Optional flag to enable cross-partition query.
        :return: List of documents matching the query.
        """
        try:
            query_options = {}
            
            if partition_key is not None:
                query_options['partition_key'] = partition_key
            
            if parameters is not None:
                query_options['parameters'] = parameters
            
            if enable_cross_partition_query is not None:
                query_options['enable_cross_partition_query'] = enable_cross_partition_query
            
            documents = list(self.container_client.query_items(query=query, **query_options))
            return documents
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error querying CosmosDB container: {e}")
            raise

    def upsert_cosmosdb_document(self, document: dict):
        """
        Insert or update a document in the Cosmos DB container.

        :param document: Document to be inserted or updated.
        """
        try:
            self.container_client.upsert_item(document)
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error inserting document into CosmosDB container: {e}")
            raise

    def patch_cosmosdb_document(self, item_id: str, partition_key: str, operations: List[Dict], etag: Optional[str] = None):
        """
        Patch a document in the Cosmos DB container using partial update.

        :param item_id: The ID of the item to patch.
        :param partition_key: The partition key of the item.
        :param operations: List of patch operations to apply.
        :param etag: Optional ETag for optimistic concurrency control.
        """
        try:
            patch_options = {}
            if etag:
                patch_options['if_match'] = etag

            result = self.container_client.patch_item(
                item=item_id,
                partition_key=partition_key,
                patch_operations=operations,
                **patch_options
            )
            return result
        except exceptions.CosmosHttpResponseError as e:
            if e.status_code == 412:  # Precondition Failed (ETag mismatch)
                logging.warning(f"ETag mismatch while patching document {item_id}: {e}")
                raise exceptions.CosmosAccessConditionFailedError(message=e.message) from e
            logging.error(f"Error patching document in CosmosDB container: {e}")
            raise