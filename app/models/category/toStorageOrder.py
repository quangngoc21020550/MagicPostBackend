import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class toStorageOrderModel(BaseModel):
    id: str = Field(..., alias='_id')
    fromType: str
    toType: str
    fromPoint: str
    toPoint: str
    responsibleBy: str
    status: str
    verifiedBy: str
    createdDate: int
    lastUpdatedDate: int

class toStorageOrderDel(BaseModel):
    id: str = Field(..., alias='_id')

class toStorageOrderSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class toStorageOrderInsmodel(BaseModel):
    fromType: str
    toType: str
    fromPoint: str
    toPoint: str
    responsibleBy: str
    status: str
    verifiedBy: str
    createdDate: int
    lastUpdatedDate: int


class toStorageOrder(modelBase):
    pass
