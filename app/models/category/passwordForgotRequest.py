import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase
from app.models import common

class passwordForgotRequestModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str

class passwordForgotRequestDel(BaseModel):
    id: str = Field(..., alias='_id')

class passwordForgotRequestSearch(BaseModel):
    content: dict
    pagesize: int
    pageindex: int

class passwordForgotRequestInsmodel(BaseModel):
    username: str


class passwordForgotRequest(modelBase):
    pass

def sendPasswordResupplyRq(userInfo, passwordForgotRequestdb, employeedb, managerdb, directordb):
    if userInfo['role'] in ['transaction-point-employee', 'gathering-point-employee']:
        try:
            managerId = list(employeedb.getModel().find({"username":userInfo["username"]}))[0]["managedBy"]
            manager = list(managerdb.getModel().find({'username': managerId}))[0]
        except:
            return (400, {'message': {'manager not found'}})
        sendPasswordResupplyInfo = {
            'username': userInfo["username"],
            'managedBy': managerId
        }
        resp = passwordForgotRequestdb.insert_doc("", json=sendPasswordResupplyInfo)
    else:
        try:
            directorId = list(directordb.getModel().find())[0]["username"]
        except:
            return (400, {'message': {'manager not found'}})
        sendPasswordResupplyInfo = {
            'username': userInfo["username"],
            'managedBy': directorId
        }
        resp = passwordForgotRequestdb.insert_doc("", json=sendPasswordResupplyInfo)
    return resp




def forgotPassword(username,userInformation, userInformationdb, passwordForgotRequestdb, employeedb, managerdb, directordb):
    if len(list(userInformationdb.getModel().find({"username": username}))) > 0:
        thisUser = list(userInformationdb.getModel().find({"username": username}))[0]
    elif len(list(userInformationdb.getModel().find({"email": username}))) > 0:
        thisUser = list(userInformationdb.getModel().find({"email": username}))[0]
        username = thisUser["username"]
    else:
        return (400, {"message": "This account not exist"})
    # role = common.getRoleFromUserInfo(thisUser)
    # if role in ["customer", "director"]:
    newPassword = common.genStaticCode(8)
    # newPassword = "abc"
    thisUser["password"] = newPassword
    if common.reset_password_via_email(thisUser["email"], newPassword):
        resp = userInformation.changePassword(thisUser, userInformationdb)
        return resp
    raise Exception("Cant send email")
    # else:
    #     resp = sendPasswordResupplyRq(thisUser, passwordForgotRequestdb, employeedb, managerdb, directordb)
    # return resp


