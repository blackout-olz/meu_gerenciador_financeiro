from datetime import datetime, timezone
from sqlmodel import Session, select
from src.modules.auth.models import User
from src.modules.auth.schemas import UserCreate, UserUpdate, EmailAlreadyInUseException
from src.core.security import hash_password
from src.core.security import verify_password
from src.core.config import Settings

settings = Settings()
DUMMY_HASHED = hash_password(settings.DUMMY_PWD)


def get_user_by_email(session: Session, email: str) -> User | None:
    """
    Busca um registro de usuário no banco de dados filtrando pelo e-mail.

    Utilizado no fluxo de login e para evitar a duplicação de cadastros.
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_cpf(session: Session, cpf: str) -> User | None:
    """
    Busca um registro de usuário no banco de dados filtrando pelo CPF.

    Utilizado para validações de unicidade antes de criar uma nova conta.
    """
    statement = select(User).where(User.cpf == cpf)
    return session.exec(statement).first()


def get_user_by_phone(session: Session, phone: str) -> User | None:
    """
    Busca um registro de usuário no banco de dados filtrando pelo telefone.

    Utilizado para garantir que dois usuários não compartilhem o mesmo número.
    """
    statement = select(User).where(User.phone == phone)
    return session.exec(statement).first()


def create_user(session: Session, user_data: UserCreate) -> User:
    """
    Persiste um novo usuário no banco de dados.

    Gera o hash seguro da senha enviada, descarta o texto limpo do payload
    e executa a transação no PostgreSQL (add, commit, refresh).
    """
    
    # 1. Gera o hash criptográfico a partir da senha em texto limpo
    hashed_pwd = hash_password(user_data.password)

    # 2. Converte o schema UserCreate para dicionário, removendo a senha original por segurança
    user_dict = user_data.model_dump(exclude={"password"})
    
    # 3. Instancia o modelo ORM (User) mesclando os dados limpos com o password_hash
    db_user = User(**user_dict, password_hash=hashed_pwd)

    # 4. Ciclo de vida de persistência do SQLModel/SQLAlchemy
    session.add(db_user)       # Prepara a instrução INSERT na transação corrente
    session.commit()           # Executa a transação permanentemente no banco
    session.refresh(db_user)   # Sincroniza o objeto Python com o registro do banco para obter ID e created_at

    return db_user


def update_user_account(session: Session, user_data: UserUpdate, db_user: User) -> User:
    """
    Atualiza os dados de perfil de um usuário existente pelo seu ID.

    Retorna a instância do usuário atualizado ou None caso o registro não exista.
    """
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if user_data.email:
        existing_user = get_user_by_email(session, user_data.email)
        if existing_user and existing_user.id != db_user.id:
            raise EmailAlreadyInUseException("E-mail já em uso.")
    
    # Extrai apenas os campos que foram efetivamente enviados pelo cliente na requisição PATCH
    user_dict = user_data.model_dump(exclude_unset=True)      
    
    # Mescla as alterações do dicionário na instância recuperada do banco
    db_user.sqlmodel_update(user_dict)
    
    # Atualiza explicitamente o campo de auditoria temporal em UTC
    db_user.updated_at = datetime.now(timezone.utc)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


def delete_user_account(session: Session, db_user: User) -> User:
    """
    Remove fisicamente (Hard Delete) um usuário do banco de dados pelo seu ID.

    Retorna o próprio objeto deletado para que o router confirme o sucesso (HTTP 204),
    ou None caso o usuário não seja localizado (HTTP 404).
    """
    
    session.delete(db_user)   # Marca a entidade para exclusão na sessão
    session.commit()          # Executa a instrução DELETE no PostgreSQL
    
    return db_user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """
    Localiza o usuário pelo e-mail e valida a senha enviada.
    Retorna a instância do User se tudo estiver correto, ou None se falhar.
    """
    user = get_user_by_email(session, email)
    if not user:
        # Prevenção a timming attacks
        verify_password(password, DUMMY_HASHED)
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user