from sqlmodel import SQLModel
from datetime import date, datetime
from uuid import UUID


class UserBase(SQLModel):
    """
    Schema Base (Data Transfer Object - DTO).

    Contém os campos públicos universais do usuário. Não possui 'table=True'
    pois serve apenas como classe pai para validação de contratos HTTP.
    """
    
    name: str
    cpf: str
    email: str
    phone: str
    birth: date | None = None
    monthly_income_estimate: int | None = None
    
    
class UserCreate(UserBase):
    """
    Schema de Entrada (Payload do POST /auth/register).

    Herda todos os campos do UserBase e exige a senha em texto limpo.
    A senha será interceptada pela camada de serviço para geração do hash antes de ir ao banco.
    """
    
    password: str
    
    
class UserResponse(UserBase):
    """
    Schema de Saída (JSON retornado pela API).

    Herda do UserBase e expõe dados gerados pelo sistema (id, created_at).
    Como 'password' e 'password_hash' não estão declarados aqui, o FastAPI
    remove essas chaves da resposta por segurança.
    """
    
    id: UUID
    created_at: datetime
    
    
class UserUpdate(SQLModel):
    """
    Schema de Entrada (Payload do PATCH /auth/update/{user_id}).
    """
    name: str | None = None
    cpf: str | None = None
    email: str | None = None
    phone: str | None = None
    birth: date | None = None
    monthly_income_estimate: int | None = None
    
    
class UserLogin(SQLModel):
    email: str
    password: str