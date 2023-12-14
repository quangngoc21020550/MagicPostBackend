import pymongo
from typing import Optional
from pydantic import BaseModel, Field

from app.models import common
from app.models.modelbase import modelBase


class packageInformationModel(BaseModel):
    id: str = Field(..., alias='_id')
    sender: str
    responsibleBy: str
    fromTransactionPoint: str
    toTransactionPoint: str
    receiverName: str
    receiverAddress: str
    receiverPhone: str
    packageType: int
    instruction: int
    status: str
    createdDate: int
    lastUpdatedDate: int

class packageInfoUpdStatusModel(BaseModel):
    id: str = Field(..., alias='_id')
    status: str

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
    receiverName: str
    receiverAddress: str
    receiverPhone: str
    packageType: int
    instruction: int
    # status: str
    createdDate: int
    lastUpdatedDate: int

class getPackageForCustomerModel(BaseModel):
    customerId: str
    pagesize: int = 0
    pageindex: int = 0

class getInformationForPackageModel(BaseModel):
    packageId: str

class packageInformation(modelBase):
    pass

def createPackageInfomation(packageInfo, packageInformationdb, gatheringPointdb, transactionPointdb):
    packageInfo["status"] = "transporting"
    if not common.checkPointExist(packageInfo["toTransactionPoint"], 'transaction', gatheringPointdb, transactionPointdb):
        raise Exception("To transaction point not exist")
    resp = packageInformationdb.insert_doc("",json=packageInfo)
    return resp

def updatePackageStatus(packageId, status, packageInformationdb):
    try:
        thisPackage = list(packageInformationdb.getModel().find({"_id": packageId}))[0]
    except:
        raise Exception("Package not found")
    thisPackage["status"] = status
    resp = packageInformationdb.update_doc("", json=thisPackage)
    return resp

def getPackageForCustomer(getInfo, packagedb):
    pagesize = getInfo["pagesize"]
    pageindex = getInfo["pageindex"]
    customerId = getInfo["customerId"]
    return 200, list(packagedb.getModel().find({"sender": customerId}).sort('createdDate', -1).limit(pagesize).skip(pagesize* (pageindex-1)))

def getInfoForPackage(getInfo, toStoragedb, toCustomerdb):
    packageId = getInfo["packageId"]
    return 200, list(toStoragedb.getModel().find({"packageId": packageId}).sort('createdDate', -1)) + list(toCustomerdb.getModel().find({"packageId": packageId}).sort('createdDate', -1))

