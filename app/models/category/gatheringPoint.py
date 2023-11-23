import pymongo
from typing import Optional
from pydantic import BaseModel, Field

from app.models import common
from app.models.modelbase import modelBase


class gatheringPointModel(BaseModel):
    id: str = Field(..., alias='_id')
    name: str
    code: str
    managedBy: Optional[str] = None
    createdDate: int
    lastUpdatedDate: int

class gatheringPointDel(BaseModel):
    id: str = Field(..., alias='_id')

class gatheringPointSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class gatheringPointInsmodel(BaseModel):
    name: str
    code: str
    managedBy: Optional[str] = None
    createdDate: int
    lastUpdatedDate: int


class gatheringPoint(modelBase):
    pass

class getAllGatheringPointModel(BaseModel):
    pagesize: int
    pageindex: int

class getAllGatheringPointBelongingsModel(BaseModel):
    gatheringPointId : str
    pagesize: int
    pageindex: int

class gatheringPointUpdManagerModel(BaseModel):
    pointId: str
    managedBy: str

def gatheringPointInsert(gatheringPointInfo, gatheringPointdb):
    resp = gatheringPointdb.insert_doc("", json=gatheringPointInfo)
    return resp

def getAllPoint(getInfo, pointdb):
    pagesize = getInfo["pagesize"]
    pageindex = getInfo["pageindex"]
    return 200, list(pointdb.getModel().find().sort('createdDate', -1).limit(pagesize).skip(pagesize* (pageindex-1)))

def getAllBelongings(getInfo,transpointdb):
    gatheringPointId = getInfo["gatheringPointId"]
    pagesize = getInfo["pagesize"]
    pageindex = getInfo["pageindex"]
    return 200, list(transpointdb.getModel().find({"belongsTo":gatheringPointId}).sort('createdDate', -1).limit(pagesize).skip(pagesize* (pageindex-1)))

