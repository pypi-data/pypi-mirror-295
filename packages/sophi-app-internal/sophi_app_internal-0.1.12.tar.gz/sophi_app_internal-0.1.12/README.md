# `sophi-app-internal` Python Package

## Overview
sophi-app-internal is a Python package designed to facilitate secure and authenticated HTTP request handling, particularly in environments where JWT (JSON Web Token) authentication is used. The package includes utilities for validating JWTs, fetching public keys, constructing HTTP request objects with robust header and parameter management, and interacting with Azure Cosmos DB.

## Features
- JWT validation and verification using Auth0.
- Secure fetching of JSON Web Key Sets (JWKS).
- Construction and management of HTTP request objects with headers, parameters, and body handling.
- Azure Cosmos DB client for querying and managing documents.

## Installation

To install the sophi-app-internal package, use the following command:


```bash
pip install sophi-app-internal
```

## Token Validator Usage
### Setting Up Variables
Before using the package, ensure you have set up the necessary variables:

- AUTH0_DOMAIN: Your Auth0 domain, e.g. `<tenant>.us.auth0.com`.
- AUDIENCE: The expected token audience. **You need to [register your API](https://auth0.com/docs/get-started/auth0-overview/set-up-apis) on Auth0 before getting a valid audience value**.

You can set these variables in your environment:

```python
auth0_domain = "app-dev.us.auth0.com"
audience = [
    "https://api.example.com/",
    "https://website.us.auth0.com/userinfo"
  ]
token = "<your token>"
```
Note: ensure you pass the token after parsing the `Authorization` header and removing the `Bearer` keyword.

### Example Code
Validating JWTs
Here's an example of how to validate a JWT using the token_validator function.

```python
from sophi_app_internal import token_validator

try:
    claims = token_validator(token, audience, auth0_domain)
    print(claims)
except Exception as e:
    print(e)
```

## Cosmos DB Client Usage

### Setting Up Variables

Before using the Cosmos DB client, ensure you have set up the necessary variables:

- COSMOS_CONNECTION_STRING: Your Azure - Cosmos DB connection string.
- DB_NAME: The name of your database.
- CONTAINER_NAME: The name of your container.

You can set these variables in your environment:

```python
import os

connection_string = os.getenv("COSMOS_CONNECTION_STRING")
db_name = "your_db_name"
container_name = "your_container_name"
```

### Example Code
#### Using CosmosContainerClient
Here's an example of how to use the CosmosContainerClient to query and manage documents in Azure Cosmos DB.

```python
import os
import logging
from sophi_app_internal import CosmosContainerClient

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up connection variables
connection_string = os.getenv("COSMOS_CONNECTION_STRING")
db_name = "your_db_name"
container_name = "your_container_name"

# Initialize the client
client = CosmosContainerClient(connection_string, db_name, container_name)

# Query from the initial container
query = "SELECT * FROM c"
user_id = "1234"
partition_key = [user_id]
documents = client.query_cosmosdb_container(query, partition_key)
print(documents)

# Switch to a different database and container
new_db_name = "another_db_name"
new_container_name = "another_container_name"
client.set_database_and_container(new_db_name, new_container_name)

# Query from the new container
documents = client.query_cosmosdb_container(query)
print(documents)

# Upsert a document
document = {
    "id": "1",
    "name": "Sample Document",
    "description": "This is a sample document."
}
client.upsert_cosmosdb_document(document)
```