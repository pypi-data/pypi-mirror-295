from auth0.authentication import GetToken
from auth0.management import Auth0
from dotenv import load_dotenv
import os

load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

class Auth0ClientManager:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = Auth0ManagementApiClient()
        return cls._client

class Auth0ManagementApiClient:
    def __init__(self):
        self.auth0 = self.auth0_management_api_client()

    def auth0_management_api_client(self):
        get_token = GetToken(AUTH0_DOMAIN, AUTH0_CLIENT_ID, client_secret=AUTH0_CLIENT_SECRET)
        token = get_token.client_credentials('https://{}/api/v2/'.format(AUTH0_DOMAIN))
        mgmt_api_token = token['access_token']

        auth0 = Auth0(AUTH0_DOMAIN, mgmt_api_token)
        return auth0

    def fetch_user_by_email(self, email):
        user = self.auth0.users_by_email.search_users_by_email(email)
        return user[0]
    
    def fetch_user_by_id(self, user_id):
        user = self.auth0.users.get(user_id)
        return user

    def fetch_access_tokens(self, user_id):
        user_identities = self.auth0.users.get(user_id, fields=['identities'])
        access_tokens = []
        for identity in user_identities['identities']:
            access_tokens.append({
                'provider': identity['provider'],
                'access_token': identity['access_token']
            })

        return access_tokens
