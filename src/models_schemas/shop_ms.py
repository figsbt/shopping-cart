from typing import Optional
from pydantic import BaseModel, Field
from rdb_store.dbops import Base, Column, String, Integer, Float, PrimaryKeyConstraint


class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, nullable=False, primary_key=True)
    item_name = Column(String(225), nullable=False)
    item_details = Column(String(225), nullable=False)
    stock = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)

    PrimaryKeyConstraint("id", name="pk_user_id")


class ItemBaseSchema(BaseModel):
    item_name: str
    item_details: str
    stock: int
    cost: float


class ItemCreateSchema(ItemBaseSchema):
    pass


class ItemSchema(ItemBaseSchema):
    id: int

    class Config:
        orm_mode = True


# class Cart(Base):
#     __tablename__ = 'carts'

#     id = Column(Integer, nullable=False, primary_key=True, index=True)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         nullable=False, server_default=text("now()"))
#     updated_at = Column(TIMESTAMP(timezone=True),
#                         nullable=False, server_default=text("now()"))

#     products = relationship("Product", back_populates="owner")


# class Product(Base):
#     __tablename__ = 'products'

#     id = Column(Integer, nullable=False, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     price = Column(Float, nullable=False)
#     description = Column(String, nullable=False)
#     category = Column(String, nullable=False)
#     image = Column(String, nullable=True)
#     rating = Column(String, nullable=True)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         nullable=False, server_default=text("now()"))
#     updated_at = Column(TIMESTAMP(timezone=True),
#                         nullable=False, server_default=text("now()"))
#     owner_id = Column(Integer, ForeignKey("carts.id"))

#     owner = relationship("Cart", back_populates="products")