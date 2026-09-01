from uuid import UUID
from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from jwt.exceptions import InvalidTokenError

from src.modules.auth.models import User
from src.core.database import get_session
from src.modules.auth.schemas import UserCreate, UserResponse, UserUpdate, Token
from src.modules.auth.services import (
    authenticate_user,
    create_user,
    delete_user_account,
    get_user_by_cpf,
    get_user_by_email,
    get_user_by_phone,
    update_user_account,
)
from src.core.config import Settings
from src.core.security import create_access_token
from src.modules.auth.dependencies import get_current_user

settings = Settings()
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

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


@router.post("/token")
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    session: Session = Depends(get_session)
    ) -> Token:
    """
    Autentica o usuário validando credenciais.
    Retorna erro genérico 401 para impedir enumeração de e-mails ativos.
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    print(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def get_user(current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
    """Retorna o perfil do usuário autenticado."""
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_user(current_user: Annotated[User, Depends(get_current_user)], user_data: UserUpdate, session: Session = Depends(get_session)):
    """Atualiza parcialmente as informações de perfil do usuário."""
    updated_user = update_user_account(session, user_data, current_user)
    
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado no sistema."
        )

    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: Annotated[User, Depends(get_current_user)], session: Session = Depends(get_session)):
    """Remove permanentemente a conta de um usuário (Hard Delete)."""
    delete_user_account(session, current_user)

    return None