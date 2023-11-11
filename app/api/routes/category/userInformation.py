from fastapi.responses import JSONResponse
# from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from fastapi import APIRouter, Body, Depends, HTTPException, status, Request, Response, Header
from fastapi.encoders import jsonable_encoder
from typing import List
# from app.core.utilscm import  authrequire
# from app.core.utilscm.authrequire import get_current_user
# from app.callcache import dict_cache
from app.models.category import userInformation, userInformationdb, customer, customerdb, employeedb, employee,  \
                    director, directordb, manager, managerdb


router = APIRouter()
# security = HTTPBasic()


@router.post("/sign-up")
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
        resp = userInformation.signUp(encoded_body, userInformationdb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400, content={'message': str(e)})


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

# @router.post("/director-sign-up")
# # @authrequire.check_roles_required(roles_required=["admin"])
# async def insedrt(
#     body: userInformation.userInformationSignUpmodel = Body(..., embed=True),
#         # current_user: dict = Depends(get_current_user),request : Request = None
# ):
#     # wrong_get_error = HTTPException(
#     #     status_code=HTTP_400_BAD_REQUEST,
#     #     detail=strings.INCORRECT_INPUT,
#     # )
#     try:
#         encoded_body = jsonable_encoder(body)
#         roles = ['customer', 'director']
#         resp1 = userInformation.signUp(encoded_body, userInformationdb, roles)
#         directorModel = {
#             'username': encoded_body.get('username'),
#             'createdDate': encoded_body.get('createdDate'),
#             'lastUpdatedDate': encoded_body.get('lastUpdatedDate')
#         }
#         resp2 = director.directorSignUp(directorModel, directordb)
#         if resp2[0] != resp1[0]:
#             raise Exception("insert to db error")
#         return JSONResponse(status_code=resp1[0],content=resp1[1])
#     except Exception as e:
#         return JSONResponse(status_code=400,content={'message': str(e)})

# @router.post("/company-member-sign-up")
# # @authrequire.check_roles_required(roles_required=["admin"])
# async def insedrt(
#     body: userInformation.companyMemberSignUpmodel = Body(..., embed=True),
#         # current_user: dict = Depends(get_current_user),request : Request = None
# ):
#     # wrong_get_error = HTTPException(
#     #     status_code=HTTP_400_BAD_REQUEST,
#     #     detail=strings.INCORRECT_INPUT,
#     # )
#     try:
#         encoded_body = jsonable_encoder(body)
#         role = encoded_body.get('role')
#         roles = ["customer", role]
#         managedBy = encoded_body.get('managedBy')
#         encoded_body.pop('managedBy')
#         resp = userInformation.signUp(encoded_body, userInformationdb, roles)
#         return JSONResponse(status_code=resp[0],content=resp[1])
#     except Exception as e:
#         return JSONResponse(status_code=400, content={'message': str(e)})

@router.get("/get")
async def get(validate_token: str = Header("")):
    try:
        resp = userInformation.getUser(validate_token)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400, content={'message': str(e)})

