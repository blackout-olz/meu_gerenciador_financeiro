from sqlmodel import Field, SQLModel
from datetime import date, datetime, timezone
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str
    cpf: str = Field(unique=True)
    email: str = Field(unique=True)
    phone: str = Field(unique=True)
    birth: date | None = Field(default=None)
    password_hash: str
    monthly_income_estimate: int | None = Field(default=0)
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )