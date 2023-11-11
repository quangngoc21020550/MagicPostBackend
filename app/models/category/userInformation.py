import jwt
import pymongo
from typing import Optional, List
from pydantic import BaseModel, Field

from app.config import SECRET_KEY, SECURITY_ALGORITHM
from app.models import common
from app.models.modelbase import modelBase
from starlette import status

class userInformationModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str
    password: str
    roles: List[str]
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
    roles: List[str]
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
    roles: List[str]
    createdDate: int
    lastUpdatedDate: int

def signUp(userInformation, userinformationdb):
    username = userInformation.get('username').lower()
    password = userInformation.get('password')
    if len(list(userinformationdb.getModel().find({"username": username}))) != 0:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Username had already used"})
    hashedPassword = common.hash_password(password, username)
    userInformationOut = userInformation.copy()
    userInformationOut["password"] = hashedPassword
    resp = userinformationdb.insert_doc("", json=userInformationOut)
    return resp

def login(loginInformation, userinformationdb):
    username = loginInformation.get('username').lower()
    password = loginInformation.get('password')
    hashedPassword = common.hash_password(password, username)
    try:
        thisUser = list(userinformationdb.getModel().find({"username": username}))[0]
    except:
        return (status.HTTP_400_BAD_REQUEST,{"message": "This account has not been signed up"})

    if thisUser["password"] == hashedPassword:
        to_encode = {
            'username': thisUser['username'],
            'roles': thisUser['roles']
        }
        encoded_jwt = common.generate_token(to_encode)

        return (status.HTTP_200_OK, {'validate_token':str(encoded_jwt, 'utf-8')})
    else:
        return (status.HTTP_400_BAD_REQUEST, {"message": "Wrong password"})

def getUser(validate_token):
    try:
        return (status.HTTP_200_OK, common.getUserInfoByToken(bytes(validate_token, 'utf-8')))
    except:
        return (status.HTTP_400_BAD_REQUEST, {'message': "Invalid token"})

def getRolesFromUserInfo(userInfo):
    try:
        return userInfo['roles']
    except:
        return []
