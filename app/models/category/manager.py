import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class managerModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str
    type: str
    pointManaged: str
    createdDate: int
    lastUpdatedDate: int

class managerDel(BaseModel):
    id: str = Field(..., alias='_id')

class managerSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class managerInsmodel(BaseModel):
    username: str
    type: str
    pointManaged: str
    createdDate: int
    lastUpdatedDate: int


class manager(modelBase):
    pass
