from typing import List

from sophi_app_internal.Intergrations.Auth0.token_validation import verify_jwt


def token_validator(token: str, audience: List[str], auth0_domain: str) -> dict:
    """
    Validate the authorization token

    Args:
        token: The JWT token to be verified.
        audience list: The audience of the token.
        auth0_domain: The Auth0 domain, e.g. <tenant>.us.auth0.com

    Returns:
        dict: The claims from the verified JWT token.

    Raises:
        Exception: If the token is expired or verification fails
    """
    
    claims = verify_jwt(token, audience, auth0_domain)
    if not claims:
        raise Exception("Unauthorized no claims found")
    return claims

