from concurrent.futures import ThreadPoolExecutor

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

def getPackageForCustomer(getInfo, packagedb,toStorageOrderdb,toCustomerOrderdb, transactionPointdb, gatheringPointdb):
    pagesize = getInfo["pagesize"]
    pageindex = getInfo["pageindex"]
    customerId = getInfo["customerId"]

    def getPointName(pkg):
        try:
            listStrOrder = list(toStorageOrderdb.getModel().find({"packageId": pkg['_id']}))
            listCusOrder = list(toCustomerOrderdb.getModel().find({"packageId": pkg['_id']}))
            message = "Đang lưu trữ tại "
            type = ""
            toCus = len(listCusOrder) > 0
            if toCus:
                lastOrder = listCusOrder[len(listCusOrder) - 1]
                if lastOrder['status'] == 'transporting':
                    pkg["message"] = "Đang vận chuyển tới tay người nhận"
                    return pkg
                elif lastOrder['status'] == 'received':
                    pkg["message"] = "Đã vận chuyển tới tay người nhận"
                    return pkg
                else:
                    pointId = lastOrder["fromPoint"]
                    storageName = list(transactionPointdb.getModel().find({"_id": pointId}))[0]['name']
                    pkg['message'] = "Đang lưu trữ tại " + storageName
                    return pkg
            listTrans = listStrOrder
            try:
                lastOrder = listTrans[len(listTrans)-1]
                # pointId = ""
                if lastOrder['status'] == 'transporting':
                    message = "Đang vận chuyển tới "
                    pointId = lastOrder["toPoint"]
                    type = lastOrder["toType"]
                elif lastOrder['status'] == 'received':
                    pointId = lastOrder["toPoint"]
                    type = lastOrder["toType"]
                else:
                    pointId = lastOrder["fromPoint"]
                    type = lastOrder["fromType"]
            except Exception:
                pointId = pkg["fromTransactionPoint"]
                type = 'transaction'

            # currStorage = None
            if type == 'transaction':
                pointdb = transactionPointdb
                message += "điểm giao dịch "
            else:
                pointdb = gatheringPointdb
                message += "điểm tập kết "
            storageName = list(pointdb.getModel().find({"_id": pointId}))[0]['name']
            # pkg["pointName"] = storageName
            # pkg['pointType'] = type
            pkg['message'] = message + storageName

        except Exception:
            pass
        return pkg

    listPackage = list(packagedb.getModel().find({"sender": customerId}).sort('createdDate', -1).limit(pagesize).skip(pagesize* (pageindex-1)))
    pool = ThreadPoolExecutor(max_workers=len(listPackage) + 1)
    listPackageWPName = list(pool.map(getPointName, listPackage))
    pool.shutdown()
    # for pkg in listPackage:
    #
    return 200, listPackageWPName


def getInfoForPackage(getInfo, toStoragedb, toCustomerdb):
    packageId = getInfo["packageId"]
    return 200, list(toStoragedb.getModel().find({"packageId": packageId}).sort('createdDate', -1)) + list(toCustomerdb.getModel().find({"packageId": packageId}).sort('createdDate', -1))

