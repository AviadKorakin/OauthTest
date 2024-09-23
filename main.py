from fastapi import FastAPI
from dotenv import load_dotenv
import os
from starlette.middleware.sessions import SessionMiddleware

from App.oauth_router import get_oauth_router

load_dotenv()

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SECRET_KEY'))

# Include the OAuth router
app.include_router(get_oauth_router())


