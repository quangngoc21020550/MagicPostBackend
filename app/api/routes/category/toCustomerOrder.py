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
from app.models.category import toCustomerOrder, toCustomerOrderdb, gatheringPointdb, transactionPointdb, employeedb, \
    storage, storagedb, packageInformationdb, packageInformation

router = APIRouter()
# security = HTTPBasic()


@router.post("/insert")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: toCustomerOrder.toCustomerOrderInsmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if not common.getRoleFromToken(validate_token) == "transaction-point-employee":
            raise Exception("No authorization")
        encoded_body = jsonable_encoder(body)
        encoded_body["status"] = "transporting"
        encoded_body["fromPoint"] = encoded_body["transactionPointId"]
        encoded_body["toPoint"] = "tay người nhận"
        if len(storage.getRecordInStorage(encoded_body["packageId"], encoded_body["transactionPointId"], storagedb))==0:
            raise Exception("Package not found in storage")
        resp = toCustomerOrder.toCustomerOrderInsert(encoded_body, toCustomerOrderdb, gatheringPointdb, transactionPointdb, employeedb, packageInformationdb)
        if resp[0] == 200:
            storage.removeFromStorage(encoded_body["packageId"], storagedb)
        # dict_cache.runApp()
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/verify")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: toCustomerOrder.toCustomerOrderModel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if not common.getRoleFromToken(validate_token) == "transaction-point-employee":
            raise Exception("No authorization")
        encoded_body = jsonable_encoder(body)
        # encoded_body["status"] = "transporting"
        resp = toCustomerOrder.toCustomerOrderVerify(encoded_body, toCustomerOrderdb, gatheringPointdb, transactionPointdb, employeedb)
        if resp[0] == 200:
            if encoded_body["status"] != "received":
                recordModel = {
                    "type": "transaction",
                    "packageId": encoded_body["packageId"],
                    "pointId": encoded_body["transactionPointId"],
                    "createdDate": encoded_body["createdDate"],
                    "lastUpdatedDate": encoded_body["lastUpdatedDate"]
                }
                resp0 = storage.insertToStorage(recordModel, storagedb)
                if resp0[0] != 200:
                    encoded_body["status"] = "transporting"
                    toCustomerOrder.toCustomerOrderVerify(encoded_body, toCustomerOrderdb, gatheringPointdb, transactionPointdb, employeedb)
                    raise ("Failed to insert to storage")
            else:
                packageInformation.updatePackageStatus(encoded_body["packageId"], "received", packageInformationdb)
        # dict_cache.runApp()
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get")
async def get():
    try:
        resp = list(toCustomerOrderdb.getModel().find())
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/get-data")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: toCustomerOrder.getDataModel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        # if not common.getRoleFromToken(validate_token) == "transaction-point-employee":
        #     raise Exception("No authorization")
        encoded_body = jsonable_encoder(body)
        # encoded_body["status"] = "transporting"
        resp = toCustomerOrder.getData(encoded_body, toCustomerOrderdb)
        # dict_cache.runApp()
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get-unverified-order")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    employeeId: str = "",
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        qr = {"$and": [
            {"responsibleBy": employeeId},
            {"status": "transporting"}
        ]}
        resp = list(toCustomerOrderdb.getModel().find(qr))
        # dict_cache.runApp()
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})



