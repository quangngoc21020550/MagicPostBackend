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
from app.models.category import userInformation, userInformationdb, customer, customerdb, employeedb, employee, \
    director, directordb, manager, managerdb, gatheringPointdb, transactionPointdb

router = APIRouter()
# security = HTTPBasic()


# @router.post("/sign-up")
# # @authrequire.check_roles_required(roles_required=["admin"])
# async def insedrt(
#     body: userInformation.userInformationSignUpmodel = Body(..., embed=True),
# validate_token: str = Header("")
#         # current_user: dict = Depends(get_current_user),request : Request = None
# ):
#     # wrong_get_error = HTTPException(
#     #     status_code=HTTP_400_BAD_REQUEST,
#     #     detail=strings.INCORRECT_INPUT,
#     # )
#     try:
#         encoded_body = jsonable_encoder(body)
#         resp = userInformation.signUp(encoded_body, userInformationdb)
#         return JSONResponse(status_code=resp[0],content=resp[1])
#     except Exception as e:
#         return JSONResponse(status_code=400, content={'message': str(e)})


@router.post("/log-in")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: userInformation.userInformationLogInModel = Body(..., embed=True),
validate_token: str = Header("")
):
    try:
        encoded_body = jsonable_encoder(body)
        resp = userInformation.login(encoded_body, userInformationdb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400, content={'message': str(e)})


@router.get("/get-user-info")
async def get(validate_token: str = Header("")):
    try:
        resp = userInformation.getUser(validate_token, userInformationdb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400, content={'message': str(e)})

@router.post("/change-password")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: userInformation.userInformationChangePasswordmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        encoded_body = jsonable_encoder(body)
        userInfo = common.getUserInfoByToken(validate_token, userInformationdb)
        if userInfo is None:
            raise Exception('Token might not exist or expired')
        userInfo["password"] = encoded_body.get('newPassword')
        resp = userInformation.changePassword(userInfo, userInformationdb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400, content={'message': str(e)})


@router.post("/customer-sign-up")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: userInformation.userInformationSignUpmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        encoded_body = jsonable_encoder(body)
        customerModel = {
            'username': encoded_body.get('username'),
            'createdDate': encoded_body.get('createdDate'),
            'lastUpdatedDate': encoded_body.get('lastUpdatedDate')
        }
        resp0 = customer.signUp(customerModel, customerdb)
        if resp0[0] != 200:
            raise Exception("insert director error")
        try:
            resp = userInformation.signUp(encoded_body, userInformationdb)
            if resp[0] != 200:
                customer.deleteAccount(resp0[1]["_id"], customerdb)
        except Exception as e:
            print(str(e))
            customer.deleteAccount(resp0[1]["_id"], customerdb)
            raise e
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400, content={'message': str(e)})


@router.post("/director-account-upsert")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: userInformation.userInformationSignUpmodel = Body(..., embed=True),
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        encoded_body = jsonable_encoder(body)
        role = "director"
        if len(list(directordb.getModel().find({'username': encoded_body.get('username')}))) > 0:
            resp = userInformation.userUpdate(encoded_body, userInformationdb)
        else:
            directorModel = {
                'username': encoded_body.get('username'),
                'createdDate': encoded_body.get('createdDate'),
                'lastUpdatedDate': encoded_body.get('lastUpdatedDate')
            }
            resp0 = director.signUp(directorModel, directordb)
            if resp0[0] != 200:
                raise Exception("insert director error")
            resp = userInformation.signUp(encoded_body, userInformationdb)
            if resp[0] != 200:
                director.deleteAcount(resp0[1]["_id"], directordb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={'message': str(e)})

@router.post("/company-member-sign-up")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: userInformation.companyMemberSignUpmodel = Body(..., embed=True),validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        encoded_body = jsonable_encoder(body)
        role = encoded_body.get('role')
        if 'gathering-point-employee' == role and common.getRoleFromToken(validate_token) not in ['gathering-point-manager', 'director']:
            raise Exception('Dont have authority')
        if 'transaction-point-employee' == role and common.getRoleFromToken(validate_token) not in ['transaction-point-manager', 'director']:
            raise Exception('Dont have authority')
        if 'gathering-point-manager' == role and common.getRoleFromToken(validate_token) != 'director':
            raise Exception('Dont have authority')
        if 'transaction-point-manager' == role and common.getRoleFromToken(validate_token) != 'director':
            raise Exception('Dont have authority')
        managedBy = encoded_body.get('managedBy')
        pointManaged = encoded_body.get('pointManaged')
        encoded_body.pop('managedBy')
        encoded_body.pop('pointManaged')
        resp0 = userInformation.companyMemberSignUp(encoded_body, role,managedBy, pointManaged,manager,employee,managerdb,employeedb,gatheringPointdb, transactionPointdb)
        if resp0[0] != 200:
            return resp0
        resp = userInformation.signUp(encoded_body, userInformationdb)
        if resp[0] != 200:
            memberId = resp0[1]["username"]
            userInformation.companyMemberDeleteAccount(memberId, role, managerdb, employeedb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400, content={'message': str(e)})


