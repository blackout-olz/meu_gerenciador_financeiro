from fastapi import FastAPI
from src.modules.auth.router import router as auth_router
from src.modules.categories.router import router as categories_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(categories_router)