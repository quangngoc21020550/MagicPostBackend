import pymongo
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class userInformationModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str
    password: str
    roles: List[str]
    createdDate: int
    lastUpdatedDate: int

class userInformationDel(BaseModel):
    id: str = Field(..., alias='_id')

class userInformationSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class userInformationInsmodel(BaseModel):
    username: str
    password: str
    roles: List[str]
    createdDate: int
    lastUpdatedDate: int


class userInformation(modelBase):
    pass
