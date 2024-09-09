import os

from sophi_app_internal.Intergrations.Microsoft.cosmos_client import CosmosContainerClient

COSMOSDB_CONNECTION_STRING = os.getenv("COSMOSDB_CONNECTION_STRING")
COSMOSDB_DATABASE_NAME = os.getenv("COSMOSDB_DATABASE_NAME")
COSMOSDB_CONTAINER_NAME = os.getenv("COSMOSDB_CONTAINER_NAME")
    

def cosmos_db_client_initialization():
    cosmos_db_client = CosmosContainerClient(COSMOSDB_CONNECTION_STRING, COSMOSDB_DATABASE_NAME, COSMOSDB_CONTAINER_NAME)
    return cosmos_db_client


