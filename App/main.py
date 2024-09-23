from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
from oauth_router import oauth_router

load_dotenv()

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SECRET_KEY'))

# Include the OAuth router
app.include_router(oauth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the GitHub OAuth demo!"}
