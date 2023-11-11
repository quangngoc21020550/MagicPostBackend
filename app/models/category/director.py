import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class directorModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str
    # info ....
    createdDate: int
    lastUpdatedDate: int

class directorDel(BaseModel):
    id: str = Field(..., alias='_id')

class directorSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class directorInsmodel(BaseModel):
    username: str
    # info ....
    createdDate: int
    lastUpdatedDate: int


class director(modelBase):
    pass

def signUp(directorInfo, directordb):
    resp = directordb.insert_doc("", json=directorInfo)
    return resp
