from rdb_store.dbops import Session
from models_schemas.shop_ms import Item, ItemCreateSchema


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
