from sqlmodel import SQLModel
from datetime import date, datetime
from uuid import UUID


class UserBase(SQLModel):
    name: str
    cpf: str
    email: str
    phone: str
    birth: date | None = None
    monthly_income_estimate: int | None = None
    
    
class UserCreate(UserBase):
    password: str
    
    
class UserResponse(UserBase):
    id: UUID
    created_at: datetime