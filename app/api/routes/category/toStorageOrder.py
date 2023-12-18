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
from app.models.category import toStorageOrder, toStorageOrderdb, gatheringPointdb, transactionPointdb, employeedb, \
    storage, storagedb, transactionPoint

router = APIRouter()
# security = HTTPBasic()


@router.post("/insert")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    toStorageOrder: toStorageOrder.toStorageOrderInsmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        ct = jsonable_encoder(toStorageOrder)
        resp = toStorageOrderdb.insert_doc("", json=ct)
        # dict_cache.runApp()
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/transaction-to-gathering")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: toStorageOrder.toStorageOrderInsmodel = Body(..., embed=True),
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
        encoded_body["fromType"] = "transaction"
        encoded_body["toType"] = "gathering"
        if len(storage.getRecordInStorage(encoded_body["packageId"], encoded_body["fromPoint"], storagedb)) == 0:
            raise Exception("Package not found in storage")

        encoded_body["toPoint"] = transactionPoint.transactionPointGetGatheringPoint(transactionPointId=encoded_body["fromPoint"], transactionPointdb=transactionPointdb)
        resp = toStorageOrder.toStorageOrderInsert(encoded_body, toStorageOrderdb, gatheringPointdb, transactionPointdb, employeedb)
        if resp[0] == 200:
            storage.removeFromStorage(resp[1]["packageId"], storagedb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/gathering-to-gathering")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: toStorageOrder.toStorageOrderInsmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if not common.getRoleFromToken(validate_token) == "gathering-point-employee":
            raise Exception("No authorization")
        encoded_body = jsonable_encoder(body)
        encoded_body["fromType"] = "gathering"
        encoded_body["toType"] = "gathering"
        if len(storage.getRecordInStorage(encoded_body["packageId"], encoded_body["fromPoint"], storagedb))==0:
            raise Exception("Package not found in storage")
        resp = toStorageOrder.toStorageOrderInsert(encoded_body, toStorageOrderdb, gatheringPointdb, transactionPointdb, employeedb)
        if resp[0] == 200:
            storage.removeFromStorage(resp[1]["packageId"], storagedb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/gathering-to-transaction")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: toStorageOrder.toStorageOrderInsmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if not common.getRoleFromToken(validate_token) == "gathering-point-employee":
            raise Exception("No authorization")
        encoded_body = jsonable_encoder(body)
        encoded_body["fromType"] = "gathering"
        encoded_body["toType"] = "transaction"
        if len(storage.getRecordInStorage(encoded_body["packageId"], encoded_body["fromPoint"], storagedb))==0:
            raise Exception("Package not found in storage")
        resp = toStorageOrder.toStorageOrderInsert(encoded_body, toStorageOrderdb, gatheringPointdb, transactionPointdb, employeedb)
        if resp[0] == 200:
            storage.removeFromStorage(resp[1]["packageId"], storagedb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/verify-order")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: toStorageOrder.toStorageOrderVerifymodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        encoded_body = jsonable_encoder(body)

        resp = toStorageOrder.toStorageOrderVerify(encoded_body, toStorageOrderdb, employeedb)
        if resp[0] == 200:
            if resp[1]["status"] == "received":
                recordModel = {
                    "type": encoded_body["toType"],
                    "packageId": encoded_body["packageId"],
                    "pointId": encoded_body["toPoint"],
                    "createdDate": encoded_body["createdDate"],
                    "lastUpdatedDate": encoded_body["lastUpdatedDate"]
                }
                resp0 = storage.insertToStorage(recordModel, storagedb)
            else:
                recordModel = {
                    "type": encoded_body["fromType"],
                    "packageId": encoded_body["packageId"],
                    "pointId": encoded_body["fromPoint"],
                    "createdDate": encoded_body["createdDate"],
                    "lastUpdatedDate": encoded_body["lastUpdatedDate"]
                }
                resp0 = storage.insertToStorage(recordModel, storagedb)
            if resp0[0] != 200:
                encoded_body["status"] = "transporting"
                toStorageOrder.toStorageOrderVerify(encoded_body, toStorageOrderdb, employeedb)
                raise ("Failed to insert to storage")

        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get")
async def get():
    try:
        resp = list(toStorageOrderdb.getModel().find())
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get-order-way")
async def get(packageId: str = ""):
    try:
        resp = list(toStorageOrderdb.getModel().find({"packageId": packageId}))
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

