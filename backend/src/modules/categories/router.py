from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.core.database import get_session
from src.modules.categories.schemas import CategoryResponse, CategoryCreate
from src.modules.categories.services import create_category as new_category

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, session: Session = Depends(get_session)):
    
    
    created_category = new_category(session, category_data)
    
    if created_category is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Categoria com mesmo nome e tipo já cadastrada."
        )
        
    return created_category