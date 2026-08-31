from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.modules.auth.models import User
from src.core.database import get_session
from src.modules.auth.schemas import UserCreate, UserLogin, UserResponse, UserUpdate
from backend.src.modules.auth.services import (
    authenticate_user,
    create_user,
    delete_user_by_id,
    get_user_by_cpf,
    get_user_by_email,
    get_user_by_phone,
    update_user_by_id,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """Cria um novo cadastro garantindo a unicidade de e-mail, CPF e telefone."""
    if get_user_by_email(session, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado no sistema."
        )

    if get_user_by_cpf(session, user_data.cpf):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="CPF já cadastrado no sistema."
        )

    if get_user_by_phone(session, user_data.phone):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Telefone já cadastrado no sistema."
        )

    return create_user(session, user_data)


@router.post("/login", response_model=UserResponse)
def login_user(user_data: UserLogin, session: Session = Depends(get_session)):
    """
    Autentica o usuário validando credenciais.
    Retorna erro genérico 401 para impedir enumeração de e-mails ativos.
    """
    user = authenticate_user(session, user_data.email, user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    return user


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, session: Session = Depends(get_session)):
    """Busca o perfil de um usuário pelo seu ID."""
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    return db_user


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user_data: UserUpdate, session: Session = Depends(get_session)):
    """Atualiza parcialmente as informações de perfil do usuário."""
    updated_user = update_user_by_id(session, user_data, user_id)

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    return updated_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, session: Session = Depends(get_session)):
    """Remove permanentemente a conta de um usuário (Hard Delete)."""
    deleted_user = delete_user_by_id(session, user_id)

    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    return None