from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_db
from sqlalchemy import select, insert, update

from app.models.review import Review
from app.schemas import CreateReview
from app.routers.auth import get_current_user
from app.models import *

router = APIRouter(prefix='/reviews', tags=['reviews'])


@router.get('/')
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    all_review = reviews.all()
    if not all_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no reviews'
        )
    return all_review


@router.post('/')
async def add_review(db: Annotated[AsyncSession, Depends(get_db)], create_review: CreateReview, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_supplier'):
        await db.execute(insert(Review).values(product_id=create_review.product_id,
                                               comment=create_review.comment,
                                               comment_data=create_review.comment_data,
                                               user_id=get_user.get("id"),
                                               grade=create_review.grade))
        await db.commit()
        # Пересчет рейтинга товара
        result = await db.execute(select(Review).where(Review.product_id == create_review.product_id))
        reviews = result.scalars().all()
        if reviews:
            # Вычисляем средний рейтинг
            average_rating = sum(review.grade for review in reviews) / len(reviews)
        else:
            average_rating = create_review.grade  # Если нет отзывов, устанавливаем рейтинг в grade

            # Обновление рейтинга продукта
        await db.execute(
            update(Product).where(Product.id == create_review.product_id).values(rating=average_rating))
        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not authorized to use this method'
        )


@router.delete('/{review_id}')
async def delete_reviews(db: Annotated[AsyncSession, Depends(get_db)], review_id: int,
                         get_user: Annotated[dict, Depends(get_current_user)]):
    review_delete = await db.scalar(select(Review).where(Review.id == review_id))
    if review_delete is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no product found'
             )
    if get_user.get('is_admin'):
            review_delete .is_active = False
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Review delete is successful'
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
            )


@router.get('/detail/{product_slug}')
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product = await db.scalar(
        select(Product).where(Product.slug == product_slug, Product.is_active == True, Product.stock > 0))
    if product is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    return product.rating