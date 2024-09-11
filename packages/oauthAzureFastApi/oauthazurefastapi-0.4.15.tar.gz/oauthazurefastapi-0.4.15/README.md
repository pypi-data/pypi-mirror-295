## OAuthAzureFastApi

### Simple and Effective Azure OAuth2 Integration for FastAPI

OAuthAzureFastApi is a streamlined Python package that empowers you to seamlessly integrate Azure Active Directory (AAD) authentication into your FastAPI applications. It streamlines the OAuth2 flow, providing a straightforward approach to secure your API routes with Azure AD credentials.

### Requirements

- **ID Token Flow:** Ensure it's enabled under `Manage > Authentication` within your Azure App Registration.
- **User.Read Permission:** Grant this permission for Microsoft Graph access under `API Permissions`.

### Installation

Utilize pip to install the package:

```bash
pip install oauthAzureFastApi


Usage
Example FastAPI Application
This code snippet demonstrates how to establish your FastAPI application for leveraging OAuthAzureFastApi:


from fastapi import FastAPI, Depends, Request
from starlette.middleware.sessions import SessionMiddleware
from oauthAzureFastApi import OAuthApp

# Replace with your Azure AD credentials
client_id = "your-client-id"
client_secret = "your-client-secret"
tenant_id = "your-tenant-id"
redirect_uri = "http://localhost:8000/callback"
frontend_uri= "http://127.0.0.1:5500/"  

# Create the OAuth app instance
oauth_app = OAuthApp(client_id, client_secret, tenant_id, redirect_uri,frontend_uri)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-session-secret")

# Integrate the OAuth router
app.include_router(oauth_app.get_app(), prefix="")

# Secure API Endpoints using the get_current_user_from_app dependency
async def get_current_user_from_app(request: Request):
    return await oauth_app.get_current_user(request)

# Example of a secured endpoint
@app.get("/secure-data")
async def secure_data(user: dict = Depends(get_current_user_from_app)):
    """Endpoint for accessing secure data."""
    return {"message": "Secure data accessed", "user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

```
### Example Login and Token Refresh
Once your application is running, you can effortlessly access these pre-built endpoints:

### Login URL:

Navigate to http://localhost:8000/login in your web browser to initiate login using Microsoft Single Sign-On (SSO). Upon successful login, this endpoint will provide you with access_token,refresh_token and userdetails.

### Token Refresh URL:

Employ the POST endpoint http://localhost:8000/refresh-id-token to refresh the ID token. Transmit the refresh_token as a query parameter.

Example:

POST http://localhost:8000/refresh-id-token?refresh_token=<your-refresh-token>


### Securing Endpoints
To safeguard your FastAPI endpoints, incorporate the get_current_user_from_app function as a dependency. This ensures user authentication before accessing the endpoint. You can also access all user realated detail from the user parameter.

```bash
@app.get("/secure-data")
async def secure_data(user: dict = Depends(get_current_user_from_app)):
    return {"message": "Secure data accessed", "user": user}
```

By including this dependency, only authorized users possessing a valid Azure AD token will be granted access to the endpoint.

### Example frontend code to extract the access token,refresh token and user info in frontend

```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OAuth2 Test App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        .tokens {
            margin-top: 20px;
            text-align: left;
        }
        pre {
            background-color: #f4f4f4;
            padding: 15px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>

    <div id="tokenContainer" style="display:none;">
        <h3>Tokens</h3>
        <p><strong>Access Token:</strong> <span id="accessToken"></span></p>
        <p><strong>Refresh Token:</strong> <span id="refreshToken"></span></p>
        <p><strong>Session ID:</strong> <span id="sessionId"></span></p>
    
        <h3>User Info</h3>
        <p><strong>User ID:</strong> <span id="userId"></span></p>
        <p><strong>Email:</strong> <span id="userEmail"></span></p>
        <p><strong>Name:</strong> <span id="userName"></span></p>
        <p><strong>Role:</strong> <span id="userRole"></span></p>
    </div>

<script>
    // Handle page load to extract tokens from the URL fragment
    window.onload = function() {
    const hash = window.location.hash;
    if (hash) {
        const params = new URLSearchParams(hash.substring(1));  // Remove '#'
        const accessToken = params.get('access_token');
        const refreshToken = params.get('refresh_token');
        const sessionId = params.get('session_id');
        const userInfo = params.get('user_info');
        
        if (accessToken && refreshToken && sessionId && userInfo) {
            // Display tokens
            document.getElementById('accessToken').innerText = accessToken;
            document.getElementById('refreshToken').innerText = refreshToken;
            document.getElementById('sessionId').innerText = sessionId;

            // Parse user_info JSON string and display user details
            const user = JSON.parse(decodeURIComponent(userInfo));
            document.getElementById('userId').innerText = user.user_id;
            document.getElementById('userEmail').innerText = user.email;
            document.getElementById('userName').innerText = user.name;
            document.getElementById('userRole').innerText = user.role.join(', '); // Display role as comma-separated list

            document.getElementById('tokenContainer').style.display = 'block';
        }
    }
};
```
    // Simulate a login flow (you should replace the URL with your backend's login endpoint)
    document.getElementById('loginBtn').onclick = function() {
        // This would redirect to your backend login route
        window.location.href = "http://localhost:8000/login";  // Change to your backend login route
    };
</script>

</body>
</html>

### Conclusion
OAuthAzureFastApi simplifies the integration of Azure AD authentication within your FastAPI applications, offering a swift and efficient method to secure your routes. Follow the steps above to quickly implement authentication in your FastAPI application.