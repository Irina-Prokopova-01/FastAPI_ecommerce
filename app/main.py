from fastapi import FastAPI
from app.routers.category import router as category_router
from app.routers.products import router as products_router

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category_router)
app.include_router(products_router)