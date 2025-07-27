from pydantic import BaseModel
from datetime import datetime


class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None = None


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class CreateReview(BaseModel):
    comment: str | None = None
    grade: float
    product_id: int
    user_id: int
    comment_data: datetime
