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

class getRecordInStorageModel(BaseModel):
    pointId: str
    pagesize: int
    pageindex: int

class getDataInStorageModel(BaseModel):
    pointId: str
    type: str
    pagesize: int
    pageindex: int



class storage(modelBase):
    pass

def insertToStorage(recordModel, storagedb):
    return storagedb.insert_doc("", json=recordModel)

def removeFromStorage(packageId, storagedb):
    storagedb.getModel().delete_many({"packageId": packageId})

def changeStorage(recordModel, storagedb):
    packageId = recordModel["packageId"]
    removeFromStorage(packageId, storagedb)
    return insertToStorage(recordModel, storagedb)

def getRecordInStorage(packageId, pointId, storagedb):
    return list(storagedb.getModel().find({'$and': [{'packageId':packageId},
                                        {'pointId':pointId}]}))

def getPackageInStorage(getInfo, storagedb):
    pagesize = getInfo["pagesize"]
    pageindex = getInfo["pageindex"]
    pointId = getInfo["pointId"]
    return 200, list(storagedb.getModel().find({"pointId": pointId}).sort('createdDate', -1).limit(pagesize).skip(pagesize* (pageindex-1)))

def getDataInStorage(getInfo, toStoragedb, toCustomerdb):
    pagesize = getInfo["pagesize"]
    pageindex = getInfo["pageindex"]
    pointId = getInfo["pointId"]
    type = getInfo["type"]
    listToCustomer = []
    if type == "send":
        key = "fromPoint"
        query = {"$and": [
            {'transactionPointId': pointId},
            {"status": "received"}
        ]}
        listToCustomer = list(toCustomerdb.getModel().find(query).sort('createdDate', -1).limit(pagesize).skip(pagesize* (pageindex-1)))
    else:
        key = "toPoint"
    query = {"$and": [
        {key: pointId},
        {"status": "received"}
    ]}
    listToStorage = list(toStoragedb.getModel().find(query).sort('createdDate', -1).limit(pagesize).skip(pagesize* (pageindex-1)))
    return 200, listToStorage + listToCustomer