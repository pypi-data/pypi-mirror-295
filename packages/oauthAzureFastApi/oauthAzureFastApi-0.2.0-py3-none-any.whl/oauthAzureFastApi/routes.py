from fastapi import FastAPI, Depends, HTTPException, Request
from .oauth import setup_oauth
from .utils import verify_token, get_current_user
from starlette.middleware.sessions import SessionMiddleware
import httpx

def setup_routes(app: FastAPI, client_id: str, client_secret: str, tenant_id: str, redirect_uri: str):
    oauth = setup_oauth(client_id, client_secret, tenant_id, redirect_uri)
    
    app.add_middleware(SessionMiddleware, secret_key="your-session-secret")

    @app.get("/login")
    async def login(request: Request):
        redirect_uri = request.url_for('auth')
        return await oauth.azure.authorize_redirect(request, redirect_uri)

    @app.get('/callback')
    async def auth(request: Request):
        token = await oauth.azure.authorize_access_token(request)
        return {"access_token": token["id_token"], "refresh_token": token["refresh_token"]}

    @app.get("/secure-data")
    async def secure_data(user: dict = Depends(get_current_user)):
        return {"message": "Secure data accessed", "user": user}
    
    @app.post("/refresh-id-token")
    async def refresh_id_token(refresh_token: str):
        """
        API to get a new id_token using the refresh_token.
        """
        # Define the payload to send to Azure AD
        payload = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'scope': 'openid profile email'
        }

        # Send a POST request to Azure AD token endpoint
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token', data=payload)
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=f"Error: {exc.response.text}")

        # Parse the response and return the new id_token
        token_response = response.json()
        new_id_token = token_response.get("id_token")
        if new_id_token:
            return {"id_token": new_id_token}
        else:
            raise HTTPException(status_code=400, detail="Failed to retrieve id_token")