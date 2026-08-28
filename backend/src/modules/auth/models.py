from sqlmodel import Field, SQLModel
from datetime import date, datetime, timezone
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    """
    Modelo de Tabela Física (ORM).

    Representa a estrutura exata da tabela 'users' no banco PostgreSQL do Supabase.
    'table=True' avisa ao SQLModel que esta classe deve ser mapeada para o banco.
    """
    
    # Sobrescreve a convenção do SQLModel para apontar diretamente para a tabela no plural
    __tablename__ = "users"
    
    # UUID como Chave Primária. default_factory gera um novo UUIDv4 em Python caso o banco não o faça
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    
    name: str
    
    # Garantia de unicidade no banco (índices únicos evitam registros duplicados)
    cpf: str = Field(unique=True)
    email: str = Field(unique=True)
    phone: str = Field(unique=True)
    
    # Campos opcionais no formulário. Se omitidos, salvam como NULL no PostgreSQL
    birth: date | None = Field(default=None)
    
    # Armazena EXCLUSIVAMENTE a senha já criptografada (hash), nunca a senha aberta
    password_hash: str
    
    monthly_income_estimate: int | None = Field(default=0)
    
    # Registro de auditoria temporal. O uso de lambda garante que a data atual (UTC)
    # seja calculada no momento exato em que cada novo objeto for instanciado.
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )