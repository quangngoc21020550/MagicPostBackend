import pymongo
from typing import Optional
from pydantic import BaseModel, Field

from app.models import common
from app.models.modelbase import modelBase


class toStorageOrderModel(BaseModel):
    id: str = Field(..., alias='_id')
    fromType: str
    toType: str
    fromPoint: str
    toPoint: str
    responsibleBy: str
    status: Optional[str] = "transporting"
    verifiedBy: Optional[str] = None
    verifiedDate: Optional[int] = None
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
    status: Optional[str] = "transporting"
    verifiedBy: Optional[str] = None
    verifiedDate: Optional[int] = None
    createdDate: int
    lastUpdatedDate: int

class toStorageOrderVerifymodel(BaseModel):
    id: str = Field(..., alias='_id')
    status: str
    verifiedBy: Optional[str] = None
    verifiedDate: Optional[int] = None
    createdDate: int
    lastUpdatedDate: int


class toStorageOrder(modelBase):
    pass

def toStorageOrderInsert(toStorageOrderInfo, toStorageOrderdb, gatheringPointdb, transactionPointdb, employeedb):
    fromType = toStorageOrderInfo.get('fromType')
    toType = toStorageOrderInfo.get('toType')
    fromPoint = toStorageOrderInfo.get('fromPoint')
    toPoint = toStorageOrderInfo.get('toPoint')
    responsibleBy = toStorageOrderInfo.get('responsibleBy')
    if not (common.checkPointExist(fromPoint, fromType, gatheringPointdb, transactionPointdb)):
        return (400, {"message": "fromPoint not exist"})
    if not (common.checkPointExist(toPoint, toType, gatheringPointdb, transactionPointdb)):
        return (400, {"message": "toPoint not exist"})
    if not (common.checkEmployeeExist(responsibleBy, fromType, employeedb)):
        return (400, {"message": fromType + " employee not exist"})
    resp = toStorageOrderdb.insert_doc("", json=toStorageOrderInfo)
    return resp

def toStorageOrderVerify(toStorageOrderVerifyInfo, toStorageOrderdb, employeedb):
    try:
        toStorageOrderInfo = list(toStorageOrderdb.getModel().find({"_id": toStorageOrderVerifyInfo["_id"]}))[0]
    except:
        return (400, {"message": "data not found"})
    toStorageOrderInfo['status'] = toStorageOrderVerifyInfo.get('status')
    toStorageOrderInfo['verifiedBy'] = toStorageOrderVerifyInfo.get('verifiedBy')
    toStorageOrderInfo['verifiedDate'] = toStorageOrderVerifyInfo.get('verifiedDate')
    if toStorageOrderInfo['verifiedBy'] is None:
        resp = toStorageOrderdb.update_doc("", json=toStorageOrderInfo)
        return resp
    if not (common.checkEmployeeExist(toStorageOrderInfo['verifiedBy'], toStorageOrderInfo['toType'], employeedb)):
        return (400, {"message": toStorageOrderInfo['toType'] + " employee not exist"})