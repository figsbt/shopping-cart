from typing import List
from fastapi import APIRouter, Depends, Body, HTTPException, status, Request
from models_schemas.shop_ms import Item, ItemSchema, ItemCreateSchema
from rdb_store.dbops import get_db, Session
from rdb_store.shop import create_item, list_items
from app_routers.enforce_roles import check_permissions


router = APIRouter()


@router.post('/add_item', response_model=ItemCreateSchema)
def add_item(
	req: Request,
	payload: ItemCreateSchema = Body(), 
	session: Session=Depends(get_db)
):
	_admin = check_permissions(req=req, session=session)
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
