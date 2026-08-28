from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import Column, Enum as SQLEnum
from sqlmodel import Field, SQLModel
from src.shared.enums import TransactionType

class Category(SQLModel, table=True):
    """
    Modelo de Tabela Física (ORM).

    Mapeia a estrutura exata da tabela 'categories' no PostgreSQL.
    Suporta categorias globais (sistema) e personalizadas por usuário.
    """
    
    # Sobrescreve a convenção do SQLModel para apontar diretamente para a tabela no plural
    __tablename__ = "categories"
        
    # Chave primária UUIDv4 gerada automaticamente no lado do servidor Python
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
        
    name: str
    
    # Chave estrangeira (FK) que vincula a categoria a um usuário específico.
    # Quando `user_id` for NULL, indica uma categoria padrão global do sistema.
    user_id: UUID | None = Field(default=None, foreign_key="users.id")
    
    # Mapeamento do tipo ENUM nativo do PostgreSQL ('transaction_type')
    # O `sa_column` força o SQLAlchemy a utilizar o tipo ENUM já existente no banco de dados
    transaction_type: TransactionType = Field(
        sa_column=Column(
            SQLEnum(TransactionType, name="transaction_type"),
            nullable=False
        )
    )
    
    icon: str
    
    # Auditoria temporal com timezone UTC resolvido no momento da instanciação
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )