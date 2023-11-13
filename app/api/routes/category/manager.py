from fastapi.responses import JSONResponse
# from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from fastapi import APIRouter, Body, Depends, HTTPException, status, Request, Response, Header
from fastapi.encoders import jsonable_encoder
from typing import List
# from app.core.utilscm import  authrequire
# from app.core.utilscm.authrequire import get_current_user
# from app.callcache import dict_cache
from app.models import common
from app.models.category import manager, managerdb, gatheringPointdb, transactionPointdb, userInformationdb, employeedb, \
    userInformation, employee

router = APIRouter()
# security = HTTPBasic()


@router.post("/insert")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: manager.managerInsmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if 'director' != common.getRoleFromToken(validate_token):
            raise Exception("Not authenticated")
        encoded_body = jsonable_encoder(body)
        resp = manager.signUp(encoded_body, managerdb, gatheringPointdb, transactionPointdb, employee, employeedb)
        return JSONResponse(status_code=resp[0], content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get")
async def get():
    try:
        resp = list(managerdb.getModel().find())
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})


@router.post("/delete")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: manager.managerDel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        encoded_body = jsonable_encoder(body)
        authorUser = common.getUserInfoByToken(validate_token, userInformationdb)
        try:
            managerDeleled = list(managerdb.getModel().find({'username': encoded_body.get('username')}))[0]
        except:
            raise Exception('data not found')
        if authorUser["role"] != 'director':
            raise Exception('No authorization')
        userInformation.companyMemberDeleteAccount(encoded_body.get('username'), 'transaction-point-manager', managerdb, employeedb)
        managerdb.getModel().delete_one({'username': encoded_body.get('username')})
        employee.deleteEmployeesManager(managerDeleled["pointManaged"], employeedb)
        manager.deletePointManager(managerDeleled["type"], managerDeleled["pointManaged"], gatheringPointdb, transactionPointdb)
        return JSONResponse(status_code=status.HTTP_200_OK, content={ 'deleted':  encoded_body.get('username')})
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/get-list-manager")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: manager.managerGetListModel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if common.getRoleFromToken(validate_token) != 'director':
            raise Exception('No authorization')
        encoded_body = jsonable_encoder(body)
        type = encoded_body.get('type')
        pointId = encoded_body.get('pointId')
        pagesize = encoded_body.get('pagesize')
        pageindex = encoded_body.get('pageindex')
        resp = manager.getListManager(type, pointId, pagesize, pageindex, managerdb)
        return JSONResponse(status_code=resp[0], content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})
