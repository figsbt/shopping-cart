import jwt
from typing import Any, Dict
from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
from models_schemas.users_ms import User, UserSchema, CreateUserSchema, UserLoginSchema, SuspendUserSchema
from rdb_store.dbops import get_db, Session
from rdb_store.users import create_user, get_user, db_suspend_user
from settings import SECRET_KEY
from app_routers.enforce_roles import check_permissions


router = APIRouter()


@router.post('/create_account', response_model=UserSchema)
def create_account(
	payload: CreateUserSchema = Body(), 
	session: Session=Depends(get_db)
):
	payload.pwd_hash = User.hash_pwd(payload.pwd_hash)
	try:
		_user = create_user(session, user=payload)
		return _user
	except Exception as ex:
		raise HTTPException(status_code=500, detail=str(ex))
	


@router.post('/login', response_model=Dict)
def login(
		payload: UserLoginSchema = Body(),
		session: Session = Depends(get_db)
	):
	try:
		user:User = get_user(session=session, email=payload.email)
	except Exception as ex:
		print(ex)
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials!")
	is_active:bool = user.is_active
	
	if not is_active:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User suspended!")
	
	is_validated:bool = user.validate_password(payload.password)
	if not is_validated:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials!")

	return user.generate_token()


@router.post('/suspend_user', response_model=Dict)
def suspend_user(
		req: Request,
		payload: SuspendUserSchema = Body(),
		session: Session = Depends(get_db)
	):
	_admin, uid = check_permissions(req=req, session=session)
	if _admin:
		db_suspend_user(session=session, email=payload.suspend_email)
		return {"Message": f"Suspended <{payload.suspend_email}> !"}
	else:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token!")
