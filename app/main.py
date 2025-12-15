from fastapi import FastAPI
from .utils import models
from .utils.database import engine
from .users import router as user_router
from .category import router as category_router
from .budgetrule import router as budget_router
from .income import router as income_router
from .savings import router as savings_router
from .expense import router as expense_router
from .wishlist import router as wishlist_router

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(user_router.router)
app.include_router(category_router.router)
app.include_router(budget_router.router)
app.include_router(income_router.router)
app.include_router(savings_router.router)
app.include_router(expense_router.router)
app.include_router(wishlist_router.router)