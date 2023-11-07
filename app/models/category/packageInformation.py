import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class packageInformationModel(BaseModel):
    id: str = Field(..., alias='_id')
    sender: str
    responsibleBy: str
    fromTransactionPoint: str
    toTransactionPoint: str
    status: str
    createdDate: int
    lastUpdatedDate: int

class packageInformationDel(BaseModel):
    id: str = Field(..., alias='_id')

class packageInformationSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class packageInformationInsmodel(BaseModel):
    sender: str
    responsibleBy: str
    fromTransactionPoint: str
    toTransactionPoint: str
    status: str
    createdDate: int
    lastUpdatedDate: int


class packageInformation(modelBase):
    pass
