import jwt
from fastapi import HTTPException, status, Request, Depends
from settings import SECRET_KEY
from rdb_store.users import get_user
from rdb_store.dbops import Session
from models_schemas.users_ms import User



def check_permissions(req: Request, session: Session, admin_check: bool = True):
	try:
		authorization = req.headers["Authorization"]
	except:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header!")
	try:
		_d = jwt.decode(authorization, SECRET_KEY, algorithms="HS256")
	except:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature verification failed!")
	if not isinstance(_d, dict) or not _d.get("email"):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad token!")
	user:User = get_user(session=session, email=_d.get("email"))
	if (admin_check) and (not user.is_admin):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not admin!")
	return True
