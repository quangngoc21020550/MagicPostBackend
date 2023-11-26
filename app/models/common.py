import datetime
import hashlib
import re

import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from random import randint
import dns
import jwt
import string
import random

from loguru import logger

from app import config


def hash_password(password, username):
    # adding 5gz as password
    salt = username

    saltedPassword = password + salt
    # Encoding the password
    hashed = hashlib.md5(saltedPassword.encode())

    # Printing the Hash
    return hashed.hexdigest()


def getUserInfoByToken(validate_token, userdb):
    try:
        userAuth = jwt.decode(validate_token, config.SECRET_KEY, algorithm=config.SECURITY_ALGORITHM)
        return list(userdb.getModel().find({"username": userAuth["username"]}))[0]
    except:
        return None


def getRoleFromUserInfo(userInfo):
    try:
        return userInfo['role']
    except:
        return None


def getRoleFromToken(validate_token):
    try:
        return jwt.decode(validate_token, config.SECRET_KEY, algorithm=config.SECURITY_ALGORITHM)['role']
    except:
        return None


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

def getPoint(pointId, type,gatheringPointdb, transactionPointdb):
    if type == 'gathering' and len(list(gatheringPointdb.getModel().find({"_id": pointId}))) > 0:
        return list(gatheringPointdb.getModel().find({"_id": pointId}))[0]
    if type == 'transaction' and len(list(transactionPointdb.getModel().find({"_id": pointId}))) > 0:
        return list(transactionPointdb.getModel().find({"_id": pointId}))[0]
    return None

def checkManagerExist(managerId, type, managerdb):
    try:
        manager = list(managerdb.getModel().find({"username": managerId}))[0]
    except Exception:
        return False
    if manager['type'] != type:
        return False
    return True

def getManager(managerId, managerdb):
    try:
        manager = list(managerdb.getModel().find({"username": managerId}))[0]
    except Exception:
        return None
    return manager

def checkEmployeeExist(employeeId, type, employeedb):
    try:
        employee = list(employeedb.getModel().find({"username": employeeId}))[0]
    except Exception:
        return False
    if employee['type'] != type:
        return False
    return True

def getCustomer(customerId, customerdb):
    try:
        return list(customerdb.getModel().find({"username": customerId}))[0]
    except Exception:
        return None


def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


def reset_password_via_email(email, newPassword):
    try:
        # Generate a random password
        password = newPassword

        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = 'noreply@example.com'
        msg['To'] = email
        msg['Subject'] = 'Password Reset'
        body = f'Your new password is: {password}'
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('hanquangngoc08@gmail.com', 'eulh jzkc bqcm xefz')
        text = msg.as_string()
        server.sendmail('noreply@example.com', email, text)
        server.quit()

        return True
    except Exception as e:
        # Log the error
        logger.info(f"Error: {e}")
        return False

def send_email(email, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'noreply@example.com'
        msg['To'] = email
        msg['Subject'] = 'Password Reset'
        body = f'{message}'
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('hanquangngoc08@gmail.com', 'eulh jzkc bqcm xefz')
        text = msg.as_string()
        code = server.sendmail('noreply@example.com', email, text)
        server.quit()
        if code == 250:
            return True
        return False
    except Exception as e:
        # Log the error
        logger.info(f"Error: {e}")
        return False

def email_verify(email):
    try:
        domain_name = email.split('@')[1]
        records = dns.resolver.resolve(domain_name, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        host = socket.gethostname()
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mxRecord)
        server.helo(host)
        server.mail('hanquangngoc08@gmail.com')
        code, message = server.rcpt(email)
        server.quit()
        if code == 250:
            return True
        return False
    except Exception as e:
        logger.info(f"Error: {e}")
        return False
    # try:
    #     server = smtplib.SMTP('smtp.gmail.com', 587)
    #     server.starttls()
    #     server.login('hanquangngoc08@gmail.com', 'eulh jzkc bqcm xefz')
    #     server.mail('hanquangngoc08@gmail.com')
    #     code, message = server.rcpt(email)
    #     server.quit()
    #     return True
    # except Exception as e:
    #     logger.info(f"Error: {e}")
    #     return False



def generate_random_string(num:int):
        return ''.join(random.sample(string.ascii_lowercase, num))

def genStaticCode(numlen:int = 8):
    randomCode = generate_random_string(numlen)
    return randomCode
