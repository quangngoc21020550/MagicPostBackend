import datetime
import hashlib

import jwt

from app import config


def hash_password(password, username):
    # adding 5gz as password
    salt = username

    saltedPassword = password + salt
    # Encoding the password
    hashed = hashlib.md5(saltedPassword.encode())

    # Printing the Hash
    return hashed.hexdigest()


def getUserInfoByToken(validate_token):
    return jwt.decode(validate_token, config.SECRET_KEY, algorithm=config.SECURITY_ALGORITHM)


def getRolesFromUserInfo(userInfo):
    try:
        return userInfo['roles']
    except:
        return []


def getRolesFromToken(validate_token):
    try:
        return getRolesFromUserInfo(getUserInfoByToken(validate_token))
    except:
        return []


def generate_token(to_encode):
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=config.TOKEN_EXPIRED
    )
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.SECURITY_ALGORITHM)
    return encoded_jwt

def checkPointExist(pointId, type,gatheringPointdb, transactionPointdb):
    if type == 'gathering' and len(list(gatheringPointdb.getModel().find({"_id": pointId}))) > 0:
        return True
    if type == 'transaction' and len(list(transactionPointdb.getModel().find({"_id": pointId}))) > 0:
        return True
    return False

def checkManagerExist(managerId, type, managerdb):
    try:
        manager = list(managerdb.getModel().find({"_id": managerId}))[0]
    except Exception:
        return False
    if manager['type'] != type:
        return False
    return True
