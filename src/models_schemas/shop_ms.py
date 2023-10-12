from typing import Optional
from pydantic import BaseModel, Field
from rdb_store.dbops import Base, Column, String, Integer, Float, PrimaryKeyConstraint, UniqueConstraint, JSON


class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, nullable=False, primary_key=True)
    item_name = Column(String(225), nullable=False)
    item_details = Column(String(225), nullable=False)
    stock = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)

    PrimaryKeyConstraint("id", name="pk_item_id")


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


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, nullable=False, primary_key=True)
    user_ref = Column(Integer, nullable=False)
    items_ref = Column(JSON, nullable=True)

    PrimaryKeyConstraint("id", name="pk_cart_id")
    UniqueConstraint("user_ref", name="uq_user_ref")


class CartBaseSchema(BaseModel):
    user_ref: int
    items_ref: dict



class CartSchema(CartBaseSchema):
    id: int

    class Config:
        orm_mode = True


class ItemToCartSchema(BaseModel):
    item_id: int
