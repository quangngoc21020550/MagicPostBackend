import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class customerModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str
    # info ...
    createdDate: int
    lastUpdatedDate: int

class customerDel(BaseModel):
    id: str = Field(..., alias='_id')

class customerSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class customerInsmodel(BaseModel):
    username: str
    # info ...
    createdDate: int
    lastUpdatedDate: int


class customer(modelBase):
    pass

def signUp(customerInfo, customerdb):
    resp = customerdb.insert_doc("", json=customerInfo)
    return resp

def deleteAccount(customerId, customdb):
    customdb.delete_doc("", json={'_id': customerId})