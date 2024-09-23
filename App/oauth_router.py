from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
import os


def get_oauth_router():
    # Initialize OAuth with proper config
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
        # Log the request's query parameters to check the code and state
        code = request.query_params.get('code')
        state = request.query_params.get('state')
        print(f"Received code: {code}, state: {state}")

        if not code or not state:
            raise HTTPException(status_code=400, detail="Missing code or state in the callback")

        try:
            # Exchange authorization code for access token
            token = await oauth.github.authorize_access_token(request)
            print(f"Access token response: {token}")

            if 'access_token' not in token:
                raise HTTPException(status_code=400, detail="Failed to retrieve access token")

            # Fetch user information from GitHub API
            response = await oauth.github.get('https://api.github.com/user', token=token)
            user_info = response.json()  # Extract JSON data from the httpx.Response object
            print(f"GitHub User Info: {user_info}")

        except Exception as e:
            print(f"Error during GitHub OAuth callback: {e}")
            raise HTTPException(status_code=400, detail=f"Authorization failed: {str(e)}")

        # Return the access token and user info as JSON
        return {"access_token": token['access_token'], "user_info": user_info}

    return oauth_router
