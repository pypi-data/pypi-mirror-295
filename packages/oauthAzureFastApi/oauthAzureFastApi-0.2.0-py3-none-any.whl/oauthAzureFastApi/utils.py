import httpx
from jose import jwt
from fastapi import HTTPException

def get_jwk_set(tenant_id):
    """Fetch the JSON Web Key Set (JWKS) from Azure."""
    jwks_url = f'https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys'
    response = httpx.get(jwks_url)
    response.raise_for_status()
    return response.json()

def convert_jwks_to_dict(jwks):
    """Convert JWKS to a dict of keys suitable for jose.jwt.decode."""
    key_dict = {}
    for key in jwks['keys']:
        if key['kty'] == 'RSA':
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "n": key["n"],
                "e": key["e"]
            }
            key_dict[key['kid']] = rsa_key
    return key_dict

def verify_token(token: str, client_id: str, tenant_id: str):
    """Verify JWT token with Azure public keys."""
    jwks = get_jwk_set(tenant_id)
    key_dict = convert_jwks_to_dict(jwks)

    try:
        headers = jwt.get_unverified_header(token)
        key = key_dict.get(headers['kid'])
        if key is None:
            raise HTTPException(status_code=401, detail="Invalid key ID")
        
        payload = jwt.decode(token, key, algorithms=['RS256'], audience=client_id)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTClaimsError as e:
        raise HTTPException(status_code=401, detail="Invalid claims")
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str, client_id: str, tenant_id: str):
    payload = verify_token(token, client_id, tenant_id)
    user_info = {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "name": payload.get("name")
    }
    return user_info