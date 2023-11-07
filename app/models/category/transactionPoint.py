import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class transactionPointModel(BaseModel):
    id: str = Field(..., alias='_id')
    belongsTo: str
    managedBy: str
    createdDate: int
    lastUpdatedDate: int

class transactionPointDel(BaseModel):
    id: str = Field(..., alias='_id')

class transactionPointSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class transactionPointInsmodel(BaseModel):
    belongsTo: str
    managedBy: str
    createdDate: int
    lastUpdatedDate: int


class transactionPoint(modelBase):
    pass
