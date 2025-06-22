from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
import pendulum

from app.backend.db import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    comment = Column(String, nullable=True)
    comment_data = Column(DateTime(timezone=True))
    grade = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

