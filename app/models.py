from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    category = Column(String, index=True)
    image_url = Column(String)


class ContactMessage(Base):
    __tablename__ = 'contact_messages'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    message = Column(Text)