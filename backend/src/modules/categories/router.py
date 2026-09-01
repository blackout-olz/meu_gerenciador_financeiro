from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.core.database import get_session
from src.modules.categories.schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from src.modules.categories import services as category_services
from src.modules.auth.dependencies import get_current_user
from src.modules.auth.models import User

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(current_user: Annotated[User, Depends(get_current_user)], category_data: CategoryCreate, session: Session = Depends(get_session)):
    created_category = category_services.create_category(session, category_data, current_user.id)
    
    if created_category is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Categoria com mesmo nome e tipo já cadastrada."
        )
        
    return created_category


@router.get("/", response_model=list[CategoryResponse])
def list_categories(current_user: Annotated[User, Depends(get_current_user)], session: Session = Depends(get_session)):
    listed_categories = category_services.list_categories_by_user_id(session, current_user.id)
    
    return listed_categories


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    current_user: Annotated[User, Depends(get_current_user)], 
    category_data: CategoryUpdate,
    category_id: UUID,
    session: Session = Depends(get_session),   
    ):
    updated_category = category_services.update_category_by_id(session, category_data, category_id, current_user.id)
    
    if updated_category is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Deu bigode, refatorar dps"
        )
    
    return updated_category
    
    
@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(current_user: Annotated[User, Depends(get_current_user)], category_id: UUID, session: Session = Depends(get_session)):
    deleted_category = category_services.delete_category_by_id(session, category_id, current_user.id)
    if deleted_category is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Deu bigode, refatorar dps"
        )
    return deleted_category