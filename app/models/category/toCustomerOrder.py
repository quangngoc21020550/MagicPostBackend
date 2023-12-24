import pymongo
from typing import Optional
from pydantic import BaseModel, Field

from app.models import common
from app.models.modelbase import modelBase


class toCustomerOrderModel(BaseModel):
    id: str = Field(..., alias='_id')
    packageId: str
    transactionPointId: str
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
    packageId: str
    transactionPointId: str
    responsibleBy: str
    status: str
    createdDate: int
    lastUpdatedDate: int

class getDataModel(BaseModel):
    employeeId: str = "all"
    pointId: str
    status: str
    pagesize: int
    pageindex: int

class toCustomerOrder(modelBase):
    pass

def getEndPoint(packageId, packageInformationdb):
    try:
        return list(packageInformationdb.getModel().find({"_id": packageId}))[0]["toTransactionPoint"]
    except:
        raise Exception("Data not found")

def toCustomerOrderInsert(toCustomerOrderInfo, toCustomerOrderdb, gatheringPointdb, transactionPointdb, employeedb,packageInformationdb):
    fromType = 'transaction'
    fromPoint = toCustomerOrderInfo.get('transactionPointId')
    if fromPoint != getEndPoint(toCustomerOrderInfo["packageId"], packageInformationdb):
        raise Exception('Goal point does not match')
    responsibleBy = toCustomerOrderInfo.get('responsibleBy')
    if not (common.checkPointExist(fromPoint, fromType, gatheringPointdb, transactionPointdb)):
        return (400, {"message": "fromPoint not exist"})
    # if not (common.checkPointExist(toPoint, toType, gatheringPointdb, transactionPointdb)):
    #     return (400, {"message": "toPoint not exist"})
    if not (common.checkEmployeeExist(responsibleBy, fromType, employeedb)):
        return (400, {"message": fromType + " employee not exist"})
    resp = toCustomerOrderdb.insert_doc("", json=toCustomerOrderInfo)
    return resp

def toCustomerOrderVerify(toCustomerOrderVerifyInfo, toCustomerOrderdb, gatheringPointdb, transactionPointdb, employeedb):
    try:
        toCustomerOrderInfo = list(toCustomerOrderdb.getModel().find({"_id": toCustomerOrderVerifyInfo["_id"]}))[0]
    except:
        return (400, {"message": "data not found"})
    fromType = 'transaction'
    fromPoint = toCustomerOrderVerifyInfo.get('transactionPointId')
    responsibleBy = toCustomerOrderVerifyInfo.get('responsibleBy')
    if not (common.checkPointExist(fromPoint, fromType, gatheringPointdb, transactionPointdb)):
        return (400, {"message": "fromPoint not exist"})
    # if not (common.checkPointExist(toPoint, toType, gatheringPointdb, transactionPointdb)):
    #     return (400, {"message": "toPoint not exist"})
    if not (common.checkEmployeeExist(responsibleBy, fromType, employeedb)):
        return (400, {"message": fromType + " employee not exist"})
    if toCustomerOrderInfo["status"] != "transporting":
        raise Exception("Already verified")
    resp = toCustomerOrderdb.update_doc("", json=toCustomerOrderVerifyInfo)
    return resp

def getData(getInfo, toCustomerOrderdb):
    pagesize = getInfo["pagesize"]
    pageindex = getInfo["pageindex"]
    type = getInfo["status"]
    pointId = getInfo["pointId"]
    employeeId = getInfo["employeeId"]
    query = {"$and": [
        {"transactionPointId": pointId},
    ]}
    if employeeId != "all":
        query["$and"].append({"responsibleBy": employeeId})
    if type != 'all':
        query["$and"].append({"status": type})

    return 200, list(toCustomerOrderdb.getModel().find(query).sort('createdDate', -1).limit(pagesize).skip(pagesize* (pageindex-1)))
