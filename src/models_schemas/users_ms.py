import bcrypt, jwt
from pydantic import BaseModel, EmailStr, Field
from settings import SECRET_KEY, UTF_FORMAT
from rdb_store.dbops import Base, Column, UniqueConstraint, String, Integer, Boolean, PrimaryKeyConstraint


class User(BaseModel):
	id: int
	email_id: EmailStr
	pwd_hash: str
	name: str 
	is_admin: bool


class User(Base):
	
	__tablename__ = "users"
	
	id = Column(Integer, nullable=False, primary_key=True)
	email_id = Column(String(225), nullable=False, unique=True)
	pwd_hash = Column(String(255), nullable=False)
	name = Column(String(225), nullable=False)
	is_active = Column(Boolean, default=True) 
	is_admin = Column(Boolean, default=False)
	
	UniqueConstraint("email_id", name="uq_user_email")
	PrimaryKeyConstraint("id", name="pk_user_id")
	
	@staticmethod
	def hash_pwd(password) -> str:
		_hpwd = bcrypt.hashpw(password.encode(UTF_FORMAT), bcrypt.gensalt())
		return _hpwd.decode(UTF_FORMAT)

	def validate_password(self, password) -> bool:
		return bcrypt.checkpw(password.encode(UTF_FORMAT), self.pwd_hash.encode(UTF_FORMAT))	

	def generate_token(self) -> dict:
		return {"access_token": jwt.encode({"email": self.email_id}, SECRET_KEY, algorithm="HS256")}


class UserBaseSchema(BaseModel):
	email_id: EmailStr
	name: str


class CreateUserSchema(UserBaseSchema):
	pwd_hash: str = Field(alias="password")
	is_admin: bool = Field(alias="is_admin", default=False)


class UserLoginSchema(BaseModel):
	email: EmailStr = Field(alias="email")
	password: str 


class SuspendUserSchema(BaseModel):
	suspend_email: EmailStr = Field(alias="suspend_email")
	

class UserSchema(UserBaseSchema):
	id: int
	is_admin: bool = Field(default=False)

	class Config:
		orm_mode = True
