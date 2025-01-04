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

origins = ["http://localhost:3000", "http://127.0.0.1:8000"]
#origins = ["*", "https://2a24-41-90-34-213.ngrok-free.app", "https://e3d1-41-90-34-213.ngrok-free.app"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, contact, users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000", "http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(blog.router, prefix="/api/v1", tags=["blog"])
app.include_router(contact.router, prefix="/api/v1", tags=["contact"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.mount("/static", StaticFiles(directory="static"), name="images")
