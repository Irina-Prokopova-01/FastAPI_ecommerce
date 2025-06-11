from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from app.models.products import Product
from sqlalchemy import insert
from slugify import slugify
from sqlalchemy import select
from sqlalchemy import update
from app.schemas import CreateProduct

from app.backend.db_depends import get_db

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products(db: Annotated[Session, Depends(get_db)]):
    products = db.execute(select(Product).where(Product.is_active == True)).all()
    if products is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no products'
        )
    return products


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[Session, Depends((get_db))], create_product: CreateProduct):
    db.execute((insert(Product).values(
        name=create_product.name,
        slug=slugify(create_product.name),
        description=create_product.description,
        price=create_product.price,
        image_url=create_product.image_url,
        stock=0,
        rating=0.0
    )))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/{category_slug}')
async def product_by_category(category_slug: str):
    pass


@router.get('/detail/{product_slug}')
async def product_detail(product_slug: str):
    pass


@router.put('/{product_slug}')
async def update_product(product_slug: str):
    pass


@router.delete('/{product_slug}')
async def delete_product(product_slug: str):
    pass