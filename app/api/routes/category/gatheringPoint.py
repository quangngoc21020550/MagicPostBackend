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
from app.models.category import gatheringPoint, gatheringPointdb, manager, managerdb, employee, employeedb, \
    transactionPointdb, transactionPoint

router = APIRouter()
# security = HTTPBasic()


@router.post("/insert")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: gatheringPoint.gatheringPointInsmodel = Body(..., embed=True),
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
        resp = gatheringPoint.gatheringPointInsert(body, gatheringPointdb)
        # dict_cache.runApp()
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get")
async def get():
    try:
        resp = list(gatheringPointdb.getModel().find())
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/delete")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: gatheringPoint.gatheringPointDel = Body(..., embed=True),
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
        numTransPointLeft = len(list(transactionPointdb.getModel().find({"belongsTo": pointId})))
        if numTransPointLeft + numEmployeeLeft + numManagerLeft > 0:
            raise Exception('Still workers or transaction points left')
        resp = gatheringPointdb.delete_doc("", json=body)
        return JSONResponse(status_code=resp[0],content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.post("/change-manager")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: gatheringPoint.gatheringPointUpdManagerModel = Body(..., embed=True),
    validate_token: str = Header("")
):
    try:
        if 'director' != common.getRoleFromToken(validate_token):
            raise Exception("Must be director to perform")
        body = jsonable_encoder(body)
        pointId = body.get('pointId')
        try:
            thisGathPoint = list(gatheringPointdb.getModel().find({"_id": pointId}))[0]
            thisManager = common.getManager(body.get('managedBy'), managerdb)
        except:
            raise Exception('data to found')
        if not common.checkManagerExist(body.get('managedBy'), 'gathering', managerdb):
            raise Exception('gathering point not exist')
        if thisGathPoint["managedBy"] is not None:
            raise Exception("this point already have manager")
        thisGathPoint["managedBy"] = body.get('managedBy')
        resp = gatheringPointdb.update_doc("", json=thisGathPoint)
        if resp[0] == 200:
            # thisManager = list(managerdb.getModel().find({'_id': body.get('managedBy')}))
            # if len(thisManager) > 0:
            #     thisManager = thisManager[0]
            oldPointId = thisManager["pointManaged"]
            manager.deletePointManager('gathering', oldPointId, gatheringPointdb, transactionPointdb)
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
    body: gatheringPoint.gatheringPointModel = Body(..., embed=True),
    validate_token: str = Header("")
):
    try:
        if 'director' != common.getRoleFromToken(validate_token):
            raise Exception("Must be director to perform")
        body = jsonable_encoder(body)
        resp = gatheringPointdb.update_doc("", json=body)
        return JSONResponse(status_code=resp[0], content=resp[1])

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

