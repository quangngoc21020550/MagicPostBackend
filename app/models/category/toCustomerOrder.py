import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class toCustomerOrderModel(BaseModel):
    id: str = Field(..., alias='_id')
    responsibleBy: str
    status: str
    createdDate: int
    lastUpdatedDate: int

class toCustomerOrderDel(BaseModel):
    id: str = Field(..., alias='_id')

class toCustomerOrderSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class toCustomerOrderInsmodel(BaseModel):
    responsibleBy: str
    status: str
    createdDate: int
    lastUpdatedDate: int


class toCustomerOrder(modelBase):
    pass
