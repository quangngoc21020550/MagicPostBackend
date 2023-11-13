import pymongo
from typing import Optional
from pydantic import BaseModel, Field

from app.models import common
from app.models.modelbase import modelBase


class employeeModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str
    type: str
    # info ....
    managedBy: str
    pointManged: str
    createdDate: int
    lastUpdatedDate: int

class employeeDel(BaseModel):
    username: str

class employeeSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class employeeInsmodel(BaseModel):
    username: str
    type: str
    # info ....
    managedBy: str
    pointManged: str
    createdDate: int
    lastUpdatedDate: int

class employeePointGetListModel(BaseModel):
    type: str
    pointId: str
    pagesize: int = 0
    pageindex: int = 0

class employeeManagerGetListModel(BaseModel):
    type: str
    managerId: str
    pagesize: int = 0
    pageindex: int = 0

class changePoint(BaseModel):
    employeeId: str
    type: str
    newPointId: str

class employee(modelBase):
    pass


def signUp(employeeInfo, employeedb,managerdb, gatheringPointdb, transactionPointdb):
    try:
        if common.getManager(employeeInfo["managedBy"], managerdb)["pointManaged"] == \
                common.getPoint(employeeInfo["pointManaged"], employeeInfo["type"], gatheringPointdb, transactionPointdb)["_id"]:
            resp = employeedb.insert_doc("", json=employeeInfo)
            return resp
        else:
            return (400, {'message': "manager do not mananged this point"})
    except Exception as e:
        raise Exception('"manager or point not exist"')

def deleteEmployeesManager(pointManaged, employeedb):
    listEmployee = employeedb.getModel().find({'pointManaged': pointManaged})
    for empl in listEmployee:
        empl["managedBy"] = None
        employeedb.update_doc("", json=empl)

def updateEmployeesManager(managerId, pointManaged, employeedb):
    listEmployee = employeedb.getModel().find({'pointManaged': pointManaged})
    for empl in listEmployee:
        empl["managedBy"] = managerId
        employeedb.update_doc("", json=empl)

def updateEmployeesPoint(managerId, pointManaged, employeedb):
    listEmployee = employeedb.getModel().find({'managedBy': managerId})
    for empl in listEmployee:
        empl["pointManaged"] = pointManaged
        employeedb.update_doc("", json=empl)

def getListEmployeeByPoint(type, pointId, pagesize, pageindex, employeedb):
    query = { "$and": [
        {"pointManaged": pointId}, {"type": type}
        ]
    }
    if pointId == "all":
        query = {"type": type}
    listEmployee = list(employeedb.getModel().find(query).limit(pagesize).skip((pageindex-1)*pagesize).sort('createdDate', -1))
    return (200, listEmployee)

def getListEmployeeByManager(type, managerId, pagesize, pageindex, employeedb):
    query = { "$and": [
        {"managedBy": managerId}, {"type": type}
        ]
    }
    if managerId == "all":
        query = {"type": type}
    listEmployee = list(employeedb.getModel().find(query).limit(pagesize).skip((pageindex-1)*pagesize).sort('createdDate', -1))
    return (200, listEmployee)

def changePointEmployee(newType,employeeId, pointId, employeedb,gatheringPointdb, transactionPointdb):
    try:
        thisEmployee = list(employeedb.getModel().find({'username': employeeId}))[0]
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