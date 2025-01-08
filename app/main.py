# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from . import models
from .database import engine
from .routers import blog, contact, users
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import re

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8001",
    "https://blogging-site-frontend.vercel.app",
    "https://blogging-site-frontend-gf461iusa-jeffetales-projects.vercel.app",
]

# Function to validate origins with regex
def is_valid_origin(origin: Optional[str]) -> bool:
    if not origin:
        return False
    allowed_patterns = [
        r"^https://blogging-site-frontend-[a-zA-Z0-9-]+-jeffetales-projects\.vercel\.app$",
        *[re.escape(o) for o in origins]
    ]
    return any(re.match(pattern, origin) for pattern in allowed_patterns)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_origin_regex=r"https://blogging-site-frontend-[a-zA-Z0-9-]+-jeffetales-projects\.vercel\.app|http://localhost:3000|http://127.0.0.1:8000|http://localhost:8001|https://blogging-site-frontend\.vercel\.app",
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

