from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/contact/", response_model=schemas.ContactMessage)
def create_contact_message(contact_message: schemas.ContactMessageCreate, db: Session = Depends(get_db)):
    print({"message": "Message received", "data": contact_message})
    return crud.create_contact_message(db=db, contact_message=contact_message)

@router.get("/contact/{message_id}", response_model=schemas.ContactMessage)
def get_contact_message(message_id: int, db: Session = Depends(get_db)):
    contact_message = crud.get_contact_message(db, message_id)
    if not contact_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    return contact_message

@router.get("/contacts/", response_model=List[schemas.ContactMessage])
def get_all_contact_messages(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    return crud.get_all_contact_messages(db, skip=skip, limit=limit)
