# OAuthAzureFastApi

## Overview

This package provides an easy way to integrate Azure OAuth2 with FastAPI. It handles authentication with Azure Active Directory using OAuth2 and allows you to secure your FastAPI routes with authentication.

## Installation

You can install the package via pip:

```bash
pip install oauthAzureFastApi


Here’s the full content you can paste into your README.md that will maintain proper indentation and formatting on PyPI. Follow this structure:

README.md Content:
markdown
Copy code
# OAuthAzureFastApi

## Overview

This package provides an easy way to integrate Azure OAuth2 with FastAPI. It handles authentication with Azure Active Directory using OAuth2 and allows you to secure your FastAPI routes with authentication.

## Installation

You can install the package via pip:

```bash
pip install oauthAzureFastApi
Usage
To use the package, follow the steps below:

Example FastAPI Application
python
Copy code
from fastapi import FastAPI, Depends, Request
from starlette.middleware.sessions import SessionMiddleware
from oauthAzureFastApi import OAuthApp

# Set your client_id, client_secret, tenant_id, and redirect_uri
client_id = "768****************************"
client_secret = "K6w************************"
tenant_id = "04072ed********************"

# The redirect URI should be your app URL + /oauth/callback
redirect_uri = "http://localhost:8000/oauth/callback"

# Create the FastAPI app with the Azure OAuth settings
oauth_app = OAuthApp(client_id, client_secret, tenant_id, redirect_uri)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-session-secret")

# Include the router from the OAuthApp module
app.include_router(oauth_app.get_app(), prefix="/oauth")

# Use get_current_user_from_app to secure API. Authorization header should be present in the header.
async def get_current_user_from_app(request: Request):
    return await oauth_app.get_current_user(request)

# Example secured API with get_current_user_from_app
@app.get("/secure-data")
def secure_data(user: dict = Depends(get_current_user_from_app)):
    """Endpoint to access secure data."""
    return {"message": "Secure data accessed", "user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
Example Login and Token Refresh
After running the app, in the Swagger documentation (available at /docs), you can use the /login API and /refresh-id-token API directly.

/login API: Provides the access_token and refresh_token after logging in with Microsoft SSO.
/refresh-id-token API: Retrieves a new id_token using the refresh_token.
Securing Endpoints
You can secure any FastAPI endpoint by using get_current_user_from_app as a dependency, which checks the user's token for authorization.
