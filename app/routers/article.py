from fastapi import APIRouter, status, Depends, Body
from typing import List, Annotated, Union
from fastapi.encoders import jsonable_encoder
from app.database.db import db
from .auth import get_current_user
from pydantic import BaseModel, Field
from datetime import datetime
from bson.objectid import ObjectId


router = APIRouter(
  prefix="/article"
)
article_db = db.article

class Article(BaseModel):
    title:      str
    content:    str
    publish_time:   datetime = datetime.now()
    publish_by: str = None
    
@router.get('')
async def get(id: str, user: dict = Depends(get_current_user)):
    ret = article_db.find_one({"_id": ObjectId(id)})
    if ret:
        print(ret)
        return {
            "content": ret['content'],
            "title": ret['title'],
            "id": str(ret['_id']),
            "publish_by": ret['publish_by'],
            "code": 200
        }
    else:
        return {
            "code": status.HTTP_404_NOT_FOUND
        }

@router.post("")
async def post(user: dict = Depends(get_current_user), article: Article = Body(...)):
    article.publish_by = user["email"]
    ret = article_db.insert_one(jsonable_encoder(article))
    return {
        "code": 200,
        "id": str(ret.inserted_id)
    }

class ArticleList(BaseModel):
    id:            str = Field(..., alias='_id')
    title:          str
    content:        str
    publish_by:     str
    publish_time:   str

async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 50
):
    return {"q": q, "skip": skip, "limit": limit}


@router.get('/list', response_model=List[ArticleList])
async def get(query: dict = Depends(common_parameters)):
    print(query)
    ret = article_db.find().limit(query['limit']).skip(query['skip'])
    _ret = list(ret)
    for x in _ret:
        x['_id'] = str(x['_id'])
    return _ret