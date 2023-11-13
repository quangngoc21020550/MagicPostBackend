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
from app.models.category import employee, employeedb, managerdb, userInformationdb, userInformation, gatheringPointdb, \
    transactionPointdb

router = APIRouter()
# security = HTTPBasic()


@router.post("/insert")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: employee.employeeInsmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        encoded_body = jsonable_encoder(body)
        if encoded_body.get('type') == 'transaction' and \
                'transaction-point-manager' != common.getRoleFromToken(validate_token):
            raise Exception("Not authenticated")
        if encoded_body.get('type') == 'transaction' and \
                'transaction-point-manager' != common.getRoleFromToken(validate_token):
            raise Exception("Not authenticated")
        resp = employee.signUp(encoded_body, employeedb, managerdb)
        return JSONResponse(status_code=resp[0], content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})



@router.post("/delete")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: employee.employeeDel = Body(..., embed=True),
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
            employeeDeleled = list(employeedb.getModel().find({'username': encoded_body.get('username')}))[0]
        except:
            raise Exception('data not found')
        if authorUser["role"] not in ['gathering-point-manager', 'transaction-point-manager', 'director']:
            raise Exception('No authorization')
        if employeeDeleled['managedBy'] != authorUser['username'] and authorUser["role"] != 'director':
            raise Exception('No authorization')
        userInformation.companyMemberDeleteAccount(encoded_body.get('username'), 'transaction-point-employee', managerdb, employeedb)
        employeedb.getModel().delete_one({'username': encoded_body.get('username')})
        return JSONResponse(status_code=status.HTTP_200_OK, content={ 'deleted':  encoded_body.get('username')})
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})


@router.get("/get")
async def get():
    try:
        resp = list(employeedb.getModel().find())
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/get-employee-by-point")
async def insedrt(
    body: employee.employeePointGetListModel = Body(..., embed=True),
validate_token: str = Header("")
):
    try:
        encoded_body = jsonable_encoder(body)
        role = common.getRoleFromToken(validate_token)

        if role not in ['gathering-point-manager', 'transaction-point-manager', 'director']:
            raise Exception('No authorization')
        type = encoded_body.get('type')
        pointId = encoded_body.get('pointId')
        pagesize = encoded_body.get('pagesize')
        pageindex = encoded_body.get('pageindex')

        if role != 'director':
            authUser = common.getUserInfoByToken(validate_token, userInformationdb)
            try:
                thisManager = list(managerdb.getModel().find({"username": authUser["username"]}))[0]
            except:
                raise Exception('manager not found')
            if thisManager['type'] != type or thisManager["pointManaged"] != pointId:
                raise Exception('No authorization')

        resp = employee.getListEmployeeByPoint(type, pointId, pagesize, pageindex, employeedb)
        return JSONResponse(status_code=resp[0], content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message": str(e)})


@router.post("/get-employee-by-manager")
async def insedrt(
        body: employee.employeeManagerGetListModel = Body(..., embed=True),
        validate_token: str = Header("")
):
    try:
        encoded_body = jsonable_encoder(body)
        role = common.getRoleFromToken(validate_token)

        if role not in ['gathering-point-manager', 'transaction-point-manager', 'director']:
            raise Exception('No authorization')
        type = encoded_body.get('type')
        managerId = encoded_body.get('managerId')
        pagesize = encoded_body.get('pagesize')
        pageindex = encoded_body.get('pageindex')

        if role != 'director':
            authUser = common.getUserInfoByToken(validate_token, userInformationdb)
            try:
                thisManager = list(managerdb.getModel().find({"username": authUser["username"]}))[0]
            except:
                raise Exception('manager not found')
            if thisManager['type'] != type or authUser["username"] != managerId:
                raise Exception('No authorization')

        resp = employee.getListEmployeeByManager(type, managerId, pagesize, pageindex, employeedb)
        return JSONResponse(status_code=resp[0], content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

@router.post("/change-employee-point")
async def insedrt(
    body: employee.changePoint = Body(..., embed=True),
validate_token: str = Header("")
):
    try:
        encoded_body = jsonable_encoder(body)
        role = common.getRoleFromToken(validate_token)

        if role not in ['gathering-point-manager', 'transaction-point-manager', 'director']:
            raise Exception('No authorization')

        type = encoded_body.get('type')
        newPointId = encoded_body.get('newPointId')
        employeeId = encoded_body.get('employeeId')
        if not common.checkPointExist(newPointId, type, gatheringPointdb, transactionPointdb):
            raise Exception('Data not found')
        if role != 'director':
            raise Exception('No authorization')

        resp = employee.changePointEmployee(type, employeeId, newPointId, employeedb, gatheringPointdb, transactionPointdb)
        return JSONResponse(status_code=resp[0], content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message": str(e)})

