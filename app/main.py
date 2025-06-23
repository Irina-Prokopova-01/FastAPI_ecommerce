from fastapi import FastAPI
from app.routers import permission

from app.routers import auth
from app.routers.category import router as category_router
from app.routers.products import router as products_router
from app.routers.review import router as review_router

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category_router)
app.include_router(products_router)
app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(review_router)