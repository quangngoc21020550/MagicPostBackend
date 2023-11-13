import pymongo
from typing import Optional
from pydantic import BaseModel, Field

from app.models import common
from app.models.modelbase import modelBase


class managerModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str
    type: str
    pointManaged: str
    createdDate: int
    lastUpdatedDate: int

class managerDel(BaseModel):
    username: str

class managerSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class managerInsmodel(BaseModel):
    username: str
    type: str
    pointManaged: str
    createdDate: int
    lastUpdatedDate: int

class managerGetListModel(BaseModel):
    type: str
    pointId: str
    pagesize: int = 0
    pageindex: int = 0

class manager(modelBase):
    pass

def deletePointManager(type, pointId, gatheringPointdb, transactionPointdb):
    if type == 'gathering':
        pointdb = gatheringPointdb
    else:
        pointdb = transactionPointdb
    try:
        thisPoint = list(pointdb.getModel().find({"_id": pointId}))[0]
    except:
        raise Exception('point not found')

    thisPoint["managedBy"] = None
    pointdb.update_doc("", json=thisPoint)


def updatePointManager(type, managerId, pointId, gatheringPointdb, transactionPointdb):
    if type == 'gathering':
        pointdb = gatheringPointdb
    else:
        pointdb = transactionPointdb
    try:
        thisPoint = list(pointdb.getModel().find({"_id": pointId}))[0]
    except:
        raise Exception('point not found')

    thisPoint["managedBy"] = managerId
    pointdb.update_doc("", json=thisPoint)

def updateManagerPoint(managerId, pointId, managerdb):
    try:
        thisManager = list(managerdb.getModel().find({"username": managerId}))[0]
    except:
        raise Exception('manager not found')

    thisManager["pointManaged"] = pointId
    managerdb.update_doc("", json=thisManager)

def getListManager(type, pointId, pagesize, pageindex, managerdb):
    query = { "$and": [
        {"pointManaged": pointId}, {"type": type}
        ]
    }
    if pointId == "all":
        query = {"type": type}
    listManager = list(managerdb.getModel().find(query).limit(pagesize).skip((pageindex-1)*pagesize).sort('createdDate', -1))
    return (200, listManager)


def signUp(managerInfo, managerdb, gatheringPointdb, transactionPointdb, employee, employeedb):
    # resp = managerdb.insert_doc("", json=managerInfo)
    # return resp
    if common.checkPointExist(managerInfo["pointManaged"], managerInfo['type'], gatheringPointdb, transactionPointdb):
        resp = managerdb.insert_doc("", json=managerInfo)
        if resp[0] == 200:
            updatePointManager(managerInfo["type"], managerInfo["username"], managerInfo["pointManaged"], gatheringPointdb, transactionPointdb)
            employee.updateEmployeesManager(managerInfo["username"], managerInfo["pointManaged"], employeedb)
        return resp
    else:
        return (400, {'message': "manager not exist"})

def changePointEmployee(newType,employeeId, pointId, employeedb,gatheringPointdb, transactionPointdb):
    try:
        thisEmployee = list(employeeId.getModel().find({'username': employeeId}))[0]
    except:
        raise Exception('data not found')

    if not common.checkPointExist(pointId, newType, gatheringPointdb, transactionPointdb):
        raise Exception(newType + ' point not found')
    newPoint = common.getPoint(pointId, newType, gatheringPointdb, transactionPointdb)

    thisEmployee['type'] = newType
    thisEmployee['pointManaged'] = pointId
    thisEmployee['managedBy'] = newPoint["managedBy"]
    resp = employeedb.update_doc("", json=thisEmployee)
    return resp
