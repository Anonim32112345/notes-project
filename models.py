from sqlalchemy import Column, Integer, String, Text
from pydantic import BaseModel, Field
from database import Base

# --- Сущности для БД (SQLAlchemy) ---
class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

# --- Базовая валидация полей (Pydantic) ---
class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    
    class Config:
        from_attributes = True