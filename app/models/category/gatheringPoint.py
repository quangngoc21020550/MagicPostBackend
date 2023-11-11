import pymongo
from typing import Optional
from pydantic import BaseModel, Field

from app.models import common
from app.models.modelbase import modelBase


class gatheringPointModel(BaseModel):
    id: str = Field(..., alias='_id')
    managedBy: str
    createdDate: int
    lastUpdatedDate: int

class gatheringPointDel(BaseModel):
    id: str = Field(..., alias='_id')

class gatheringPointSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class gatheringPointInsmodel(BaseModel):
    managedBy: str
    createdDate: int
    lastUpdatedDate: int


class gatheringPoint(modelBase):
    pass

def gatheringPointInsert(gatheringPointInfo, gatheringPointdb):
    resp = gatheringPointdb.insert_doc("", json=gatheringPointInfo)
    return resp