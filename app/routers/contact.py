from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter()


@router.post("/contact/", response_model=schemas.ContactMessage)
def create_contact_message(contact_message: schemas.ContactMessageCreate, db: Session = Depends(get_db)):
    print({"message": "Message received", "data": contact_message})
    return crud.create_contact_message(db=db, contact_message=contact_message)
