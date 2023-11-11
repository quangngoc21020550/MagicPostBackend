import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase
from app.models import common

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

def transactionPointInsert(transactionPointInfo, transactionPointdb,gatheringPointdb):
    # managerId = transactionPointInfo.get('managedBy')
    gatheringPointID = transactionPointInfo.getModel('belongsTo')
    if common.checkPointExist(gatheringPointID, "gathering", gatheringPointdb, transactionPointdb):
        resp = transactionPointdb.insert_doc("", json=transactionPointInfo)
        return resp
    else:
        return (400, {'message': "gathering point not exist"})