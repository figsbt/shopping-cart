from typing import List
from fastapi import APIRouter, Depends, Body, HTTPException, status, Request
from models_schemas.shop_ms import Item, ItemSchema, ItemCreateSchema, CartSchema, ItemToCartSchema
from rdb_store.dbops import get_db, Session
from rdb_store.shop import create_item, list_items, get_cart_for_user, modify_cart
from app_routers.enforce_roles import check_permissions


router = APIRouter()


@router.post('/add_item', response_model=ItemCreateSchema)
def add_item(
	req: Request,
	payload: ItemCreateSchema = Body(), 
	session: Session=Depends(get_db)
):
	_admin, uid = check_permissions(req=req, session=session)
	if _admin:
		return create_item(session, item=payload)
	else:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token!")


@router.get("/item_list", response_model=List)
def item_list(
	req: Request,
	session: Session=Depends(get_db)
):
	check_permissions(req=req, session=session, admin_check=False)
	return list_items(session=session)


@router.get("/cart/get_cart", response_model=CartSchema)
def get_cart(
	req: Request,
	session: Session=Depends(get_db)
):
	_admin, uid = check_permissions(req=req, session=session, admin_check=False)
	return get_cart_for_user(session=session, user_id=uid)



@router.post("/cart/add_item", response_model=CartSchema)
def add_item_to_cart(
	req: Request,
	payload: ItemToCartSchema = Body(), 
	session: Session=Depends(get_db)
):
	_admin, uid = check_permissions(req=req, session=session, admin_check=False)
	current_cart = modify_cart(session=session, user_id=uid, item_id=payload.item_id, add_or_remove="add")
	return current_cart


@router.post("/cart/remove_item", response_model=CartSchema)
def remove_item_to_cart(
	req: Request,
	payload: ItemToCartSchema = Body(), 
	session: Session=Depends(get_db)
):
	_admin, uid = check_permissions(req=req, session=session, admin_check=False)
	current_cart = modify_cart(session=session, user_id=uid, item_id=payload.item_id, add_or_remove="remove")
	return current_cart
