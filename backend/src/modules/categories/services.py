from uuid import UUID
from sqlmodel import Session, select, or_
from src.modules.categories.models import Category
from src.modules.categories.schemas import CategoryCreate, CategoryUpdate

def get_category_by_user_and_name(session: Session, user_id: UUID | None, name: str) -> Category | None:
    """
    Busca uma categoria específica cadastrada para um determinado usuário e nome.
    
    Retorna a primeira ocorrência encontrada ou None caso o registro não exista.
    """
    
    statement = select(Category).where(
        Category.user_id == user_id
        ).where(
            Category.name == name
        )
    return session.exec(statement).first()


def create_category(session: Session, category_data: CategoryCreate) -> Category | None:
    """
    Persiste uma nova categoria no banco de dados.
    
    Valida previamente se já existe uma categoria com o mesmo nome e tipo de 
    transação para o usuário informado, evitando registros duplicados.
    """
    
    category_dict = category_data.model_dump()
    
    # Consulta se o usuário já possui uma categoria com o mesmo nome
    existing_category = get_category_by_user_and_name(session, category_dict["user_id"], category_dict["name"])
    
    # Bloqueia a criação caso a categoria existente possua o mesmo tipo (INCOME/EXPENSE)
    if existing_category and existing_category.transaction_type == category_dict["transaction_type"]:
        return None
    
    # Instancia o objeto ORM e realiza o ciclo de persistência no PostgreSQL
    db_category = Category(**category_dict)
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    
    return db_category


def list_categories_by_user_id(session: Session, user_id: UUID) -> list[Category]:
    """
    Lista todas as categorias visíveis para o usuário logado.
    
    Executa uma única consulta utilizando a instrução SQL 'OR' para buscar tanto 
    as categorias associadas ao `user_id` quanto as categorias padrão do sistema (`user_id` IS NULL).
    """
    
    statement = select(Category).where(
        or_(Category.user_id == user_id, Category.user_id.is_(None))
        )
    categories = list(session.exec(statement).all())
    return categories


def update_category_by_id(session: Session, category_data: CategoryUpdate, category_id: UUID) -> Category | None:
    """
    Atualiza os dados de uma categoria existente no banco por seu UUID.

    Utiliza `exclude_unset=True` para capturar apenas os campos explicitamente
    enviados na requisição (PATCH), aplicando atualizações parciais com `sqlmodel_update`.
    """
    
    # 1. Busca o registro no banco pela chave primária
    db_category = session.get(Category, category_id)
    
    # 2. Retorna None caso a categoria não seja encontrada
    if db_category is None:
        return None
    
    # 3. Converte o schema em dicionário ignorando valores não enviados
    category_dict = category_data.model_dump(exclude_unset=True)
    
    # 4. Aplica as alterações no objeto da sessão e persiste no banco
    db_category.sqlmodel_update(category_dict)
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    
    return db_category


def delete_category_by_id(session: Session, category_id: UUID) -> Category | None:
    """
    Remove permanentemente uma categoria do banco de dados (Hard Delete).

    Retorna a representação da categoria removida em caso de sucesso
    ou None caso o registro não seja localizado.
    """
    
    # 1. Busca a categoria no banco de dados pela chave primária
    db_category = session.get(Category, category_id)
    
    # 2. Retorna None se a categoria não existir
    if db_category is None:
        return None
    
    # 3. Marca o registro para exclusão na sessão e confirma a alteração no PostgreSQL
    session.delete(db_category)
    session.commit()
    
    # 4. Retorna o objeto em memória da categoria excluída
    return db_category