import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class storageModel(BaseModel):
    id: str = Field(..., alias='_id')
    type: str
    packageId: str
    pointId: str
    createdDate: int
    lastUpdatedDate: int

class storageDel(BaseModel):
    id: str = Field(..., alias='_id')

class storageSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class storageInsmodel(BaseModel):
    type: str
    packageId: str
    pointId: str
    createdDate: int
    lastUpdatedDate: int


class storage(modelBase):
    pass
