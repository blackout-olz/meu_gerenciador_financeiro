from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel
from src.shared.enums import TransactionType

class CategoryBase(SQLModel):
    """
    Schema Base (DTO).

    Define os atributos públicos fundamentais de uma categoria financeira.
    Servirá de herança para os schemas de criação e resposta da API.
    """
    
    name: str
    icon: str
    transaction_type: TransactionType
    

class CategoryCreate(CategoryBase):
    """
    Schema de Entrada (Payload do POST /categories).

    Herda os campos de CategoryBase. O `user_id` é opcional: se informado,
    vincula a categoria a um usuário específico; se for None, trata-se de
    uma categoria global do sistema.
    """
    
    user_id: UUID | None = None
    

class CategoryResponse(CategoryBase):
    """
    Schema de Saída (JSON retornado pela API).

    Retorna todos os dados da categoria acrescidos das informações geradas
    pelo banco de dados (id, created_at). O `user_id` aceita None para
    permitir a exibição de categorias padrão do sistema.
    """
    
    id: UUID
    user_id: UUID | None
    created_at: datetime
    
    
class CategoryUpdate(SQLModel):
    """
    Schema de Entrada (Payload do PATCH /categories/{category_id}).

    Todos os campos são opcionais (`| None = None`) para permitir atualizações
    parciais no registro da categoria.
    """
    
    name: str | None = None
    icon: str | None = None
    transaction_type: TransactionType | None = None