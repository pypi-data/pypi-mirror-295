from fastapi import FastAPI
from .routes import setup_routes

def create_app(client_id: str, client_secret: str, tenant_id: str, redirect_uri: str) -> FastAPI:
    app = FastAPI()
    
    setup_routes(app, client_id, client_secret, tenant_id, redirect_uri)
    
    return app