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
from app.models.category import transactionPoint, transactionPointdb, gatheringPointdb, managerdb, manager, employee, \
    employeedb, toStorageOrderdb, storagedb, toCustomerOrderdb

router = APIRouter()
# security = HTTPBasic()


@router.post("/insert")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: transactionPoint.transactionPointInsmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        body = jsonable_encoder(body)
        if 'director' != common.getRoleFromToken(validate_token):
            raise Exception("Must be director to perform")
        resp = transactionPoint.transactionPointInsert(body, transactionPointdb,gatheringPointdb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get")
async def get():
    try:
        resp = list(transactionPointdb.getModel().find())
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/delete")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: transactionPoint.transactionPointDel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if 'director' != common.getRoleFromToken(validate_token):
            raise Exception("Must be director to perform")
        body = jsonable_encoder(body)
        pointId = body.get('_id')
        numManagerLeft = len(list(managerdb.getModel().find({"pointManaged": pointId})))
        numEmployeeLeft = len(list(employeedb.getModel().find({"pointManaged": pointId})))
        if numEmployeeLeft + numManagerLeft > 0:
            raise Exception('Still workers points left')

        numOrdersLeft = len(list(toStorageOrderdb.getModel().find({"fromPoint": pointId}, {'status': 'transporting'}))) + \
                        len(list(toStorageOrderdb.getModel().find({"toPoint": pointId}, {'status': 'transporting'}))) + \
                        len(list(toCustomerOrderdb.getModel().find({"transactionPointId": pointId}, {'status': 'transporting'})))
        numPackageLeft = len(list(storagedb.getModel().find({"pointId": pointId})))
        if numOrdersLeft + numPackageLeft > 0:
            raise Exception('Still processing orders left')

        resp = transactionPointdb.delete_doc("", json=body)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/change-gathering-point")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: transactionPoint.transactionPointUpdGatheringPointModel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if 'director' != common.getRoleFromToken(validate_token):
            raise Exception("Must be director to perform")
        body = jsonable_encoder(body)
        pointId = body.get('pointId')
        try:
            thisTransPoint = list(transactionPointdb.getModel().find({"_id": pointId}))[0]
        except:
            raise Exception('data to found')
        if not common.checkPointExist(body.get('belongsTo'), 'gathering', gatheringPointdb, transactionPointdb):
            raise Exception('gathering point not exist')
        thisTransPoint["belongsTo"] = body.get('belongsTo')
        resp = transactionPointdb.update_doc("", json=thisTransPoint)

        # if resp[0] == 200 and resp[1]["_id"] is not None:
        #     pointId = resp[1]["_id"]
        #     thisManager = list(managerdb.getModel().find({'pointManaged': pointId}))
        #     if len(thisManager) > 0:
        #         thisManager = thisManager[0]
        #         manager.updateManagerPoint('transaction', thisManager['_id'], None, managerdb)
        #         employee.updateEmployeesPoint(thisManager['_id'], None, employeedb)
                # transactionPoint.transactionPointUpdateGatheringPoint(pointId, None, transactionPointdb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/change-manager")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: transactionPoint.transactionPointUpdManagerModel = Body(..., embed=True),
    validate_token: str = Header("")
):
    try:
        if 'director' != common.getRoleFromToken(validate_token):
            raise Exception("Must be director to perform")
        body = jsonable_encoder(body)
        pointId = body.get('pointId')
        try:
            thisTransPoint = list(transactionPointdb.getModel().find({"_id": pointId}))[0]
            thisManager = common.getManager(body.get('managedBy'), managerdb)
        except:
            raise Exception('data to found')
        if not common.checkManagerExist(body.get('managedBy'), 'transaction', managerdb):
            raise Exception('manager not exist')
        if thisTransPoint["managedBy"] is not None:
            raise Exception("this point already have manager")
        thisTransPoint["managedBy"] = body.get('managedBy')
        resp = transactionPointdb.update_doc("", json=thisTransPoint)
        if resp[0] == 200:
            # thisManager = list(managerdb.getModel().find({'_id': body.get('managedBy')}))
            # if len(thisManager) > 0:
            #     thisManager = thisManager[0]
            oldPointId = thisManager["pointManaged"]
            manager.deletePointManager('transaction',oldPointId , gatheringPointdb, transactionPointdb)
            thisManager["pointManaged"] = pointId
            managerdb.update_doc("", json=thisManager)
            employee.updateEmployeesManager(body.get('managedBy'), pointId, employeedb)
            employee.updateEmployeesManager(None, oldPointId, employeedb)
        return JSONResponse(status_code=resp[0], content=resp[1])

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

@router.post("/update")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: transactionPoint.transactionPointModel = Body(..., embed=True),
    validate_token: str = Header("")
):
    try:
        if 'director' != common.getRoleFromToken(validate_token):
            raise Exception("Must be director to perform")
        body = jsonable_encoder(body)
        resp = transactionPointdb.update_doc("", json=body)
        return JSONResponse(status_code=resp[0], content=resp[1])

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

@router.post("/get-transaction-points")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: transactionPoint.transactionPointSearch = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        if 'director' != common.getRoleFromToken(validate_token):
            raise Exception("Must be director to perform")
        body = jsonable_encoder(body)
        resp = transactionPoint.getAllPoint(body, transactionPointdb)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

# @router.post("/get-transaction-belong")
# # @authrequire.check_roles_required(roles_required=["admin"])
# async def insedrt(
#     body: transactionPoint.transactionPointDel = Body(..., embed=True),
# validate_token: str = Header("")
#         # current_user: dict = Depends(get_current_user),request : Request = None
# ):
#     # wrong_get_error = HTTPException(
#     #     status_code=HTTP_400_BAD_REQUEST,
#     #     detail=strings.INCORRECT_INPUT,
#     # )
#     try:
#         # if 'director' != common.getRoleFromToken(validate_token):
#         #     raise Exception("Must be director to perform")
#         body = jsonable_encoder(body)
#         resp = transactionPoint.transactionPointGetGatheringPoint(body["_id"], transactionPointdb)
#         return JSONResponse(status_code=resp[0],content=resp[1])
#     except Exception as e:
#         return JSONResponse(status_code=400,content={"message" : str(e)})