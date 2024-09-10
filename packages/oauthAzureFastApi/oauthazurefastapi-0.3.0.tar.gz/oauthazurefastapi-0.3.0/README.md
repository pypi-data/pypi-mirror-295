'http://localhost:8000/oauth/callback' set in azure redirect

from fastapi import FastAPI, Depends,Request
from starlette.middleware.sessions import SessionMiddleware
from oauthAzureFastApi import OAuthApp

# Set your client_id, client_secret, tenant_id, and redirect_uri
client_id = "768d901f-184b-43d5-8e81-db46c17348a4"
client_secret = "K6w8Q~JeMjTT_PhQRMlicNAjaMDlppGnvoek-bDG"
tenant_id = "04072ed9-369e-4740-b17b-cd326112322a"
redirect_uri = "http://localhost:8000/oauth/callback"

# Create the FastAPI app with the Azure OAuth settings
oauth_app = OAuthApp(client_id, client_secret, tenant_id, redirect_uri)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-session-secret")

# Include the router from the OAuthApp module
app.include_router(oauth_app.get_app(), prefix="/oauth")

async def get_current_user_from_app(request: Request):
    return await oauth_app.get_current_user(request)

@app.get("/secure-data")
def secure_data(user: dict = Depends(get_current_user_from_app)):
    """Endpoint to access secure data."""
    return {"message": "Secure data accessed", "user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


