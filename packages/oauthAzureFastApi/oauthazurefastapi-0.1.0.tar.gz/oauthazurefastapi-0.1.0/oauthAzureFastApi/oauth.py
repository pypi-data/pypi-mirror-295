from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

def setup_oauth(client_id: str, client_secret: str, tenant_id: str, redirect_uri: str):
    config = Config()
    oauth = OAuth(config)
    oauth.register(
        name='azure',
        client_id=client_id,
        client_secret=client_secret,
        server_metadata_url=f'https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration',
        client_kwargs={'scope': 'email openid profile User.Read offline_access'},
        redirect_uri=redirect_uri,
    )
    return oauth