from fastapi import HTTPException, status
from rdb_store.dbops import Session
from models_schemas.shop_ms import Item, ItemCreateSchema, Cart, CartBaseSchema


def create_item(session:Session, item:ItemCreateSchema):
	db_item = Item(**item.dict())
	session.add(db_item)
	session.commit()
	session.refresh(db_item)
	return db_item


def list_items(session:Session):
	return [
		{
			"id": i.id, "item_name": i.item_name, 
   			"item_details": i.item_details, "stock": i.stock, "cost": i.cost
		}
		for i in session.query(Item).all()
	]


def create_cart(session:Session, user_id: int):
	cart_dict = {"user_ref": user_id, "items_ref": dict()}
	cart = CartBaseSchema.parse_obj(cart_dict)
	db_cart = Cart(**cart.dict())
	session.add(db_cart)
	session.commit()
	session.refresh(db_cart)
	return db_cart


def get_cart_for_user(session: Session, user_id: int):
	return session.query(Cart).filter(Cart.user_ref == user_id).one()


def modify_cart(session:Session, user_id: int, item_id: int, add_or_remove: str):
	cart = session.query(Cart).filter(Cart.user_ref == user_id).one()
	item = session.query(Item).filter(Item.id == item_id).one()
	stock = item.stock
	items_dict = cart.items_ref
	str_item_id = str(item_id)
	if add_or_remove == "add":
		if stock < 1:
			raise HTTPException(status_code=404, detail=f"Not stock for {item_id}!")
		items_dict[str_item_id] = items_dict.get(str_item_id, 0) + 1
		new_stock = stock - 1
	elif add_or_remove == "remove":
		if str_item_id not in items_dict:
			raise HTTPException(status_code=404, detail=f"No {item_id} in cart!")
		item_stock = items_dict[str_item_id]
		item_stock = item_stock - 1
		if not item_stock:
			del items_dict[str_item_id]
		else:
			items_dict[str_item_id] = item_stock
		new_stock = stock + 1
	session.query(Cart).filter(Cart.user_ref == user_id).update({'items_ref': items_dict})
	session.query(Item).filter(Item.id == item_id).update({'stock': new_stock})
	session.commit()
	session.refresh(cart)
	return cart
