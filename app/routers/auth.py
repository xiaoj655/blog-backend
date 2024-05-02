from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import sys
sys.path.append('..')
from app.database.db import db
from app.schema.user import User
from passlib.context import CryptContext
from typing import Union
from datetime import datetime, timedelta, timezone
from app.utils.mail import send_verify_mail
from app.config import config
import uuid

router = APIRouter(
  prefix='/auth'
)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
user_db = db.user
verify_dict = {}
oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = config.hash_secret
ALGORITHM = "HS256"

def create_access_token(data: dict, expire_delata: Union[timedelta, None]=None):
    to_encode = data.copy()
    if expire_delata:
        expire = datetime.now(timezone.utc) + expire_delata
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=40)
    
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encode_jwt

async def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user = user_db.find_one({"email": user_email})
    if user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return user
    

@router.post('/login')
async def login(user: User):
    _user = user_db.find_one({"email": user.email})
    if not _user:
        return {
            "code": status.HTTP_404_NOT_FOUND
        }
    success = pwd_context.verify(user.password, _user["password"])
    if success:
        token = create_access_token({"sub":user.email})
        return {
            "code": status.HTTP_200_OK,
            "token": token
        }
    else:
        return {
            "code": status.HTTP_401_UNAUTHORIZED
        }

@router.post('/register', status_code=status.HTTP_200_OK)
async def post(user: User):
    _user = user_db.find_one({"email": user.email})
    if _user:
        return {
            "code": status.HTTP_409_CONFLICT
        }
    
    _uuid = uuid.uuid4()
    flag = send_verify_mail(user.email, _uuid)
    if flag:
        verify_dict.update({str(_uuid): user})
        return {
            "code": 200
        }
    else :
        return {
            "code": 500
        }

@router.get('/verify/{verify_code}', status_code=status.HTTP_200_OK)
async def verify(verify_code: str):
    if verify_code in verify_dict:
        pwd = pwd_context.hash(verify_dict[verify_code].password)
        email = verify_dict[verify_code].email
        user_db.insert_one(jsonable_encoder({"email": email, "password": pwd, 'name': ''}))
        del verify_dict[verify_code]
        return {
            "code": 200
        }
    else:
        return {
            "code": 404
        }