from fastapi import FastAPI, Depends, HTTPException, Request, APIRouter
from authlib.integrations.starlette_client import OAuth
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
import logging
from jose import jwt
import httpx

class OAuthApp:
    def __init__(self, client_id: str, client_secret: str, tenant_id: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.redirect_uri = redirect_uri

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize FastAPI app and router
        self.router = APIRouter()

        # OAuth2 provider (Azure AD)
        self.oauth = OAuth(Config(".env"))
        self.oauth.register(
            name='azure',
            client_id=self.client_id,
            client_secret=self.client_secret,
            server_metadata_url=f'https://login.microsoftonline.com/{self.tenant_id}/v2.0/.well-known/openid-configuration',
            client_kwargs={'scope': 'email openid profile User.Read offline_access'},
            redirect_uri=self.redirect_uri,
        )

        self.oauth2_scheme = OAuth2AuthorizationCodeBearer(
            authorizationUrl=f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/authorize',
            tokenUrl=f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token',
        )

        # Define routes
        self._define_routes()
        

    def _define_routes(self):
        @self.router.get("/login")
        async def login(request: Request):
            redirect_uri = request.url_for('auth')
            return await self.oauth.azure.authorize_redirect(request, redirect_uri)

        @self.router.get('/callback')
        async def auth(request: Request):
            token = await self.oauth.azure.authorize_access_token(request)
            self.logger.info("Token response: %s", token)
            return {"access_token": token["id_token"], "refresh_token": token["refresh_token"]}


        @self.router.post("/refresh-id-token")
        async def refresh_id_token(refresh_token: str):
            """
            API to get a new id_token using the refresh_token.
            """
            payload = {
                'grant_type': 'refresh_token',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': refresh_token,
                'scope': 'openid profile email'
            }

            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token', data=payload)
                    response.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    raise HTTPException(status_code=exc.response.status_code, detail=f"Error: {exc.response.text}")

            token_response = response.json()
            new_id_token = token_response.get("id_token")
            if new_id_token:
                return {"id_token": new_id_token}
            else:
                raise HTTPException(status_code=400, detail="Failed to retrieve id_token")

    def get_jwk_set(self):
        """Fetch the JSON Web Key Set (JWKS) from Azure."""
        jwks_url = f'https://login.microsoftonline.com/{self.tenant_id}/discovery/v2.0/keys'
        response = httpx.get(jwks_url)
        response.raise_for_status()
        return response.json()

    def convert_jwks_to_dict(self, jwks):
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

    def verify_token(self, token: str):
        """Verify JWT token with Azure public keys."""
        jwks = self.get_jwk_set()
        key_dict = self.convert_jwks_to_dict(jwks)

        try:
            headers = jwt.get_unverified_header(token)
            key = key_dict.get(headers['kid'])
            if key is None:
                raise HTTPException(status_code=401, detail="Invalid key ID")
            
            payload = jwt.decode(token, key, algorithms=['RS256'], audience=self.client_id)
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTClaimsError as e:
            self.logger.error("JWT Claims Error: %s", e)
            raise HTTPException(status_code=401, detail="Invalid claims")
        except jwt.JWTError as e:
            self.logger.error("JWT Error: %s", e)
            raise HTTPException(status_code=401, detail="Invalid token")
    
    async def get_current_user(self, request: Request):
        """Extract token from request header and return the current user."""
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        token = auth_header.replace("Bearer ", "", 1)  # Remove "Bearer " prefix
        if not token:
            raise HTTPException(status_code=401, detail="Token missing")

        try:
            payload = self.verify_token(token)
            user_info = {
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "name": payload.get("name")
            }
            return user_info
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

    def get_app(self):
        """Return the FastAPI router"""
        return self.router
