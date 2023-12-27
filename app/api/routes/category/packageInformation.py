
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
from app.models.category import packageInformation, packageInformationdb, gatheringPointdb, transactionPointdb, storage, \
    storagedb, customerdb, toCustomerOrderdb, toStorageOrderdb, userInformationdb

router = APIRouter()
# security = HTTPBasic()


@router.post("/insert")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: packageInformation.packageInformationInsmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        encoded_body = jsonable_encoder(body)
        customerId = encoded_body.get('sender')
        if common.getCustomer(customerId, customerdb) is None:
            raise Exception('Customer not found')
        encoded_body["_id"] = common.genStaticCode(5).upper()
        resp = packageInformation.createPackageInfomation(encoded_body,packageInformationdb, gatheringPointdb, transactionPointdb)
        # dict_cache.runApp()
        if resp[0] == 200:
            recordModel = {
                "type": "transaction",
                "packageId": resp[1]["_id"],
                "pointId": encoded_body["fromTransactionPoint"],
                "createdDate": encoded_body["createdDate"],
                "lastUpdatedDate": encoded_body["lastUpdatedDate"]
            }
            resp0 = storage.insertToStorage(recordModel, storagedb)
            if resp0[0] != 200:
                packageInformationdb.getModel().delete_one(resp[1]["_id"])
                raise ("Failed to insert to storage")
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

# @router.post("/update-status")
# # @authrequire.check_roles_required(roles_required=["admin"])
# async def insedrt(
#     body: packageInformation.packageInformationInsmodel = Body(..., embed=True),
# validate_token: str = Header("")
#         # current_user: dict = Depends(get_current_user),request : Request = None
# ):
#     # wrong_get_error = HTTPException(
#     #     status_code=HTTP_400_BAD_REQUEST,
#     #     detail=strings.INCORRECT_INPUT,
#     # )
#     try:
#         encoded_body = jsonable_encoder(body)
#         resp = packageInformation.createPackageInfomation(encoded_body,packageInformationdb, gatheringPointdb, transactionPointdb)
#         # dict_cache.runApp()
#         return JSONResponse(status_code=resp[0],content=resp[1])
#     except Exception as e:
#         return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get")
async def get():
    try:
        resp = list(packageInformationdb.getModel().find())
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})


@router.post("/get-package-info-for-customer")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: packageInformation.getPackageForCustomerModel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if not common.getRoleFromToken(validate_token) == "customer":
            raise Exception("No authorization")
        encoded_body = jsonable_encoder(body)
        resp = packageInformation.getPackageForCustomer(encoded_body, packageInformationdb, storagedb, transactionPointdb, gatheringPointdb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/get-info-for-package")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: packageInformation.getInformationForPackageModel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        # if not common.getRoleFromToken(validate_token) == "customer":
        #     raise Exception("No authorization")
        encoded_body = jsonable_encoder(body)
        resp = packageInformation.getInfoForPackage(encoded_body, toStorageOrderdb, toCustomerOrderdb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get-information")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    packageId: str = "",
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        # if not common.getRoleFromToken(validate_token) == "customer":
        #     raise Exception("No authorization")
        try:
            package = list(packageInformationdb.getModel().find({"_id": packageId}))[0]
        except Exception:
            raise Exception('data not found')
        fromPointId = package['fromTransactionPoint']
        toPointId = package['toTransactionPoint']
        try:
            fromPointName = list(transactionPointdb.getModel().find({"_id": fromPointId}))[0]['name']
            toPointName = list(transactionPointdb.getModel().find({"_id": toPointId}))[0]['name']
        except Exception:
            raise Exception('point not found')
        sender = package["sender"]
        responsibleBy = package['responsibleBy']
        try:
            senderName = list(userInformationdb.getModel().find({"username": sender}))[0]['lastName']
            emName = list(userInformationdb.getModel().find({"username": responsibleBy}))[0]['lastName']
        except Exception:
            raise Exception('user not found')

        package["fromPoint"] = fromPointName
        package["toPoint"] = toPointName
        package["senderName"] = senderName
        package["employeeName"] = emName

        return JSONResponse(status_code=200,content=package)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message": str(e)})

