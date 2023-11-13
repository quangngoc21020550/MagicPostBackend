import jwt
import pymongo
from typing import Optional, List
from pydantic import BaseModel, Field

from app import config
from app.config import SECRET_KEY, SECURITY_ALGORITHM
from app.models import common
from app.models.modelbase import modelBase
from starlette import status
from verify_email import verify_email

class userInformationModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str
    password: str
    role: str
    email: Optional[str] = None
    createdDate: int
    lastUpdatedDate: int

class userInformationDel(BaseModel):
    id: str = Field(..., alias='_id')

class userInformationSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class userInformationInsmodel(BaseModel):
    username: str
    password: str
    role: str
    email: Optional[str] = None
    createdDate: int
    lastUpdatedDate: int


class userInformation(modelBase):
    pass

class userInformationLogInModel(BaseModel):
    username: str
    password: str

class userInformationSignUpmodel(BaseModel):
    username: str
    password: str
    role: str
    email: Optional[str] = None
    familyName: Optional[str] = ""
    lastName: Optional[str] = ""
    dateOfBirth: Optional[int] = None
    createdDate: int
    lastUpdatedDate: int

class companyMemberSignUpmodel(BaseModel):
    username: str
    password: str
    role: str
    email: Optional[str] = None
    familyName: Optional[str] = ""
    lastName: Optional[str] = ""
    dateOfBirth: Optional[int] = None
    managedBy: Optional[str] = None
    pointManaged: Optional[str] = None
    createdDate: int
    lastUpdatedDate: int

class userInformationChangePasswordmodel(BaseModel):
    newPassword: str

def signUp(userInformation, userinformationdb):
    import nest_asyncio
    nest_asyncio.apply()
    username = userInformation.get('username').lower()
    password = userInformation.get('password')
    email = userInformation.get('email').lower()
    role = userInformation.get('role')
    if role not in config.VALID_ROLES:
        return (status.HTTP_400_BAD_REQUEST, {"message": "invalid role"})
    # if role == 'customer' or role == 'director':
    if email is None:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Email field must be implemented"})
    elif common.validate_email(email) is False:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Wrong email format"})
    elif verify_email(email) is False:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Email domain not exist"})
    elif len(list(userinformationdb.getModel().find({"email": email}))) != 0:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Email had already used"})
    if len(list(userinformationdb.getModel().find({"username": username}))) != 0:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Username had already used"})
    hashedPassword = common.hash_password(password, username)
    userInformationOut = userInformation.copy()
    userInformation['username'] = username
    userInformationOut["password"] = hashedPassword
    userInformation['email'] = email
    resp = userinformationdb.insert_doc("", json=userInformationOut)
    return resp

def login(loginInformation, userinformationdb):
    username = loginInformation.get('username').lower()
    if len(list(userinformationdb.getModel().find({"username": username}))) > 0:
        thisUser = list(userinformationdb.getModel().find({"username": username}))[0]
    elif len(list(userinformationdb.getModel().find({"email": username}))) > 0:
        thisUser = list(userinformationdb.getModel().find({"email": username}))[0]
        username = thisUser["username"]
    else:
        return (status.HTTP_400_BAD_REQUEST, {"message": "This account has not been signed up"})
    password = loginInformation.get('password')
    hashedPassword = common.hash_password(password, username)

    if thisUser["password"] == hashedPassword:
        to_encode = {
            'username': thisUser['username'],
            'role': thisUser['role']
        }
        encoded_jwt = common.generate_token(to_encode)

        return (status.HTTP_200_OK, {'validate_token':str(encoded_jwt, 'utf-8')})
    else:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Wrong password"})

def getUser(validate_token, userdb):
    try:
        return (status.HTTP_200_OK, common.getUserInfoByToken(bytes(validate_token, 'utf-8'), userdb))
    except:
        return (status.HTTP_400_BAD_REQUEST, {'message': "Invalid token"})

def changePassword(userInformation, userinformationdb):
    username = userInformation.get('username').lower()
    password = userInformation.get('password')
    hashedPassword = common.hash_password(password, username)
    userInformationOut = userInformation.copy()
    userInformation['username'] = username
    userInformationOut["password"] = hashedPassword
    resp = userinformationdb.update_doc("", json=userInformationOut)
    return resp

def userUpdate(userInformation, userinformationdb):
    import nest_asyncio
    nest_asyncio.apply()
    username = userInformation.get('username').lower()
    try:
        thisUser = list(userinformationdb.getModel().find({'username': username}))[0]
    except Exception:
        raise Exception('data not found')

    # password = userInformation.get('password')
    # hashedPassword = common.hash_password(password, username)
    # userInformationOut = userInformation.copy()
    # userInformation['username'] = username
    # userInformationOut["password"] = hashedPassword
    email = userInformation.get('email').lower()
    role = userInformation.get('role')
    if role not in config.VALID_ROLES:
        return (status.HTTP_400_BAD_REQUEST, {"message": "invalid role"})
    # if role == 'customer':
    if email is None:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Email field must be implemented"})
    elif common.validate_email(email) is False:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Wrong email format"})
    elif verify_email(email) is False:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Email domain not exist"})
    elif len(list(userinformationdb.getModel().find({"email": email}))) != 0:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Email had already used"})

    userInformation["_id"] = thisUser["_id"]
    userInformation["password"] = thisUser["password"]
    resp = userinformationdb.update_doc("", json=userInformation)
    return resp

def companyMemberSignUp(encoded_body, role,managedBy, pointManaged,manager,employee,managerdb,employeedb,gatheringPointdb, transactionPointdb):
    resp = 400, {'message': "invalid role"}
    if role == 'gathering-point-manager':
        managerInfo = {
            "username": encoded_body.get('username'),
            "type": "gathering",
            "pointManaged": pointManaged,
            "createdDate": encoded_body.get('createdDate'),
            "lastUpdatedDate": encoded_body.get('lastUpdatedDate')
        }
        resp = manager.signUp(managerInfo, managerdb, gatheringPointdb, transactionPointdb, employee, employeedb)
    elif role == 'transaction-point-manager':
        managerInfo = {
            "username": encoded_body.get('username'),
            "type": "transaction",
            "pointManaged": pointManaged,
            "createdDate": encoded_body.get('createdDate'),
            "lastUpdatedDate": encoded_body.get('lastUpdatedDate')
        }
        resp = manager.signUp(managerInfo, managerdb, gatheringPointdb, transactionPointdb, employee, employeedb)
    elif role == "gathering-point-employee":
        employeeInfo = {
            "username": encoded_body.get('username'),
            "type": "gathering",
            "managedBy": managedBy,
            "pointManaged": pointManaged,
            "createdDate": encoded_body.get('createdDate'),
            "lastUpdatedDate": encoded_body.get('lastUpdatedDate')
        }
        resp = employee.signUp(employeeInfo, employeedb, managerdb, gatheringPointdb, transactionPointdb)
    elif role == "transaction-point-employee":
        employeeInfo = {
            "username": encoded_body.get('username'),
            "type": "transaction",
            "managedBy": managedBy,
            "pointManaged": pointManaged,
            "createdDate": encoded_body.get('createdDate'),
            "lastUpdatedDate": encoded_body.get('lastUpdatedDate')
        }
        resp = employee.signUp(employeeInfo, employeedb, managerdb, gatheringPointdb, transactionPointdb)
    return resp

def companyMemberDeleteAccount(memberId, role, managerdb,employeedb):
    # resp = (400, {'message': "invalid role"})
    if role == 'gathering-point-manager':
        managerdb.getModel().delete_one({'username':memberId})
    elif role == 'transaction-point-manager':
        managerdb.getModel().delete_one({'username':memberId})
    elif role == "gathering-point-employee":
        employeedb.getModel().delete_one({'username':memberId})
    elif role == "transaction-point-employee":
        employeedb.getModel().delete_one({'username':memberId})
