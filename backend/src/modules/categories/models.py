from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import Column, Enum as SQLEnum
from sqlmodel import Field, SQLModel
from src.shared.enums import TransactionType

class Category(SQLModel, table=True):
    # Sobrescreve a convenção do SQLModel para apontar diretamente para a tabela no plural
    __tablename__ = "categories"
        
    # UUID como Chave Primária. default_factory gera um novo UUIDv4 em Python caso o banco não o faça
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
        
    name: str
    
    # UUID chave estrageira que referencia o User que é "dono" da categoria
    # Se for NULL, significa que a categoria é pública e do sistema
    user_id: UUID | None = Field(default=None, foreign_key="users.id")
    
    transaction_type: TransactionType = Field(
        sa_column=Column(
            SQLEnum(TransactionType, name="transaction_type"),
            nullable=False
        )
    )
    
    icon: str
    
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )