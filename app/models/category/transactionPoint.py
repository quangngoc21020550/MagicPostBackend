import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase
from app.models import common

class transactionPointModel(BaseModel):
    id: str = Field(..., alias='_id')
    name: str
    code: str
    belongsTo: str
    managedBy: Optional[str] = None
    createdDate: int
    lastUpdatedDate: int

class transactionPointUpdGatheringPointModel(BaseModel):
    pointId: str
    belongsTo: str

class transactionPointUpdManagerModel(BaseModel):
    pointId: str
    managedBy: str

class transactionPointDel(BaseModel):
    id: str = Field(..., alias='_id')

class transactionPointSearch(BaseModel):
    # content : dict
    pagesize: int
    pageindex: int

class transactionPointInsmodel(BaseModel):
    name: str
    code: str
    belongsTo: str
    managedBy: Optional[str] = None
    createdDate: int
    lastUpdatedDate: int


class transactionPoint(modelBase):
    pass

def transactionPointInsert(transactionPointInfo, transactionPointdb,gatheringPointdb):
    # managerId = transactionPointInfo.get('managedBy')
    gatheringPointID = transactionPointInfo.get('belongsTo')
    if common.checkPointExist(gatheringPointID, "gathering", gatheringPointdb, transactionPointdb):
        resp = transactionPointdb.insert_doc("", json=transactionPointInfo)
        return resp
    else:
        return (400, {'message': "gathering point not exist"})

def transactionPointUpdateGatheringPoint(gatheringPointId,newGatheringPointId, transactionPointdb):
    listTransPoint = list(transactionPointdb.getModel().find({'belongsTo': gatheringPointId}))
    for transpoint in listTransPoint:
        transpoint['belongsTo'] = newGatheringPointId
        transactionPointdb.update_doc("", json=transpoint)

def transactionPointGetGatheringPoint(transactionPointId, transactionPointdb):
    try:
        transPoint = list(transactionPointdb.getModel().find({'_id': transactionPointId}))[0]
        return transPoint['belongsTo']
    except Exception:
        raise Exception("transaction point not found")

def oneTransactionPointUpdateGatheringPoint(transactionPointId,newGatheringPointId, transactionPointdb):
    try:
        thisTransPoint = list(transactionPointdb.getModel().find({'_id': transactionPointId}))[0]
    except:
        raise Exception('transaction point not found')

    thisTransPoint['belongsTo'] = newGatheringPointId
    transactionPointdb.update_doc("", json=thisTransPoint)

def getAllPoint(getInfo, pointdb):
    pagesize = getInfo["pagesize"]
    pageindex = getInfo["pageindex"]
    return 200, list(pointdb.getModel().find().sort('createdDate', -1).limit(pagesize).skip(pagesize* (pageindex-1)))
