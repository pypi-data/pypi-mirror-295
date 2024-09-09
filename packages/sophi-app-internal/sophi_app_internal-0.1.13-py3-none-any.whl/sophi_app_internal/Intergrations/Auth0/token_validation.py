import jwt
import requests, json
from jose.exceptions import ExpiredSignatureError
from jwt.algorithms import RSAAlgorithm
from typing import List

ALGORITHMS = ["RS256"]

def get_jwks(auth0_domain: str):
    """
    Fetch the JSON Web Key Set (JWKS) from the Auth0 domain.

    Returns:
        dict: The JWKS containing public keys.
    """
    jwks_url = f"https://{auth0_domain}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    if response.status_code != 200:
        raise Exception("unable to fetch JWKS from Auth0")
    return response.json()

def verify_jwt(token: str, audience: List[str], auth0_domain: str):
    """
    Verify the JWT token using the public keys from the JWKS.

    Args:
        token (str): The JWT token to be verified.
        audience list: The audience of the token.
        auth0_domain (str): The Auth0 domain, e.g. <tenant>.us.auth0.com.

    Returns:
        dict: The claims from the verified JWT token.

    Raises:
        Exception: If the token is expired or verification fails.
    """
    try:
        jwks = get_jwks(auth0_domain)
        unverified_header = jwt.get_unverified_header(token)
        public_keys = {}
        for key in jwks['keys']:
            kid = key['kid']
            public_key = RSAAlgorithm.from_jwk(json.dumps(key))
            public_keys[kid] = public_key
        # Extract the kid from the token header
        kid = unverified_header['kid']
        if kid in public_keys:
            claims = jwt.decode(token, key=public_keys[kid], algorithms=ALGORITHMS, audience=audience, issuer=f"https://{auth0_domain}/")
            return claims
        
    except ExpiredSignatureError:
        raise Exception("Unauthorized token has expired")
    except Exception as e:
        raise Exception(e)
