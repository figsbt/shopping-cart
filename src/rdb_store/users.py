from rdb_store.dbops import Session
from models_schemas.users_ms import User, CreateUserSchema
from rdb_store.shop import create_cart


def create_user(session:Session, user:CreateUserSchema):
	db_user = User(**user.dict())
	session.add(db_user)
	session.commit()
	session.refresh(db_user)
	if db_user.id:
		create_cart(session=session, user_id=db_user.id)	
	return db_user


def get_user(session:Session, email: str):
	return session.query(User).filter(User.email_id == email).one()


def db_suspend_user(session: Session, email:str):
	session.query(User).filter(User.email_id == email).update({'is_active': False})
	session.commit()
	return
