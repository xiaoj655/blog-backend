from pydantic import BaseModel
import sys
sys.path.append('..')
from app.config import config


class User(BaseModel):
    user_name:  str = ''
    email:      str
    password:   str
