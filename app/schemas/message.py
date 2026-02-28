from pydantic import BaseModel, EmailStr

class MessageCreate(BaseModel):
    to: EmailStr
    subject: str
    body: str
