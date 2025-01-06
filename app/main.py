# app/main.py

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, contact, users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Update origins to include your vercel domain
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "https://your-frontend-domain.vercel.app"  # Add your frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(blog.router, prefix="/api/v1", tags=["blog"])
app.include_router(contact.router, prefix="/api/v1", tags=["users"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

# Only mount static files if the directory exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
