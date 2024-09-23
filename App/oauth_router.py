from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os

def get_oauth_router():
    # Load environment variables
    oauth = OAuth()

    # Register GitHub OAuth
    oauth.register(
        name='github',
        client_id=os.getenv('GITHUB_CLIENT_ID'),
        client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
        authorize_url='https://github.com/login/oauth/authorize',
        access_token_url='https://github.com/login/oauth/access_token',
        redirect_uri=os.getenv('GITHUB_REDIRECT_URI'),
        client_kwargs={'scope': 'user:email'},
    )

    oauth_router = APIRouter()

    @oauth_router.get("/login")
    async def login(request: Request):
        # Redirect the user to GitHub for authorization
        redirect_uri = os.getenv('GITHUB_REDIRECT_URI')
        return await oauth.github.authorize_redirect(request, redirect_uri)

    @oauth_router.get("/auth")
    async def auth(request: Request):
        # Get the access token from the callback request
        try:
            token = await oauth.github.authorize_access_token(request)
            user_info = await oauth.github.get('user', token=token)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Authorization failed")

        # Return some details (e.g., GitHub username)
        return {"access_token": token, "user_info": user_info}

    return oauth_router
