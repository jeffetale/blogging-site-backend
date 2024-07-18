from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, contact

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(blog.router, prefix="/api/v1", tags=["blog"]) 
app.include_router(contact.router, prefix="/api/v1", tags=["contact"])