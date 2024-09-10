'http://localhost:8000/oauth/callback' set in azure redirect

from fastapi import FastAPI, Depends,Request
from starlette.middleware.sessions import SessionMiddleware
#import OAuth from oauthAzureFastApi
from oauthAzureFastApi import OAuthApp

# Set your client_id, client_secret, tenant_id, and redirect_uri
client_id = "768****************************"
client_secret = "K6w************************"
tenant_id = "04072ed********************"

# redirect uri should be your app url+/oauth/callback
redirect_uri = "http://localhost:8000/oauth/callback"

# Create the FastAPI app with the Azure OAuth settings
oauth_app = OAuthApp(client_id, client_secret, tenant_id, redirect_uri)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-session-secret")

# Include the router from the OAuthApp module
app.include_router(oauth_app.get_app(), prefix="/oauth")

# use get_current_user_from_app to secure api. Authorization heade should be present in header.
async def get_current_user_from_app(request: Request):
    return await oauth_app.get_current_user(request)

# example secured api with get_current_user_from_app
@app.get("/secure-data")
def secure_data(user: dict = Depends(get_current_user_from_app)):
    """Endpoint to access secure data."""
    return {"message": "Secure data accessed", "user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

## after running the app in swagger doc you can see the /login api and /refresh-id-token api. you can directly use those to 
## login with microsoft SSO and get new id token using refresh token. login api will provide aceestoken and refrsh token

