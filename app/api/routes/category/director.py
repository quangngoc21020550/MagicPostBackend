from fastapi.responses import JSONResponse
# from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from fastapi import APIRouter, Body, Depends, HTTPException, status, Request, Response, Header
from fastapi.encoders import jsonable_encoder
from typing import List
# from app.core.utilscm import  authrequire
# from app.core.utilscm.authrequire import get_current_user
# from app.callcache import dict_cache
from app.models.category import director, directordb


router = APIRouter()
# security = HTTPBasic()


@router.post("/insert")
# @authrequire.check_roles_required(roles_required=["admin"])
async def insedrt(
    body: director.directorInsmodel = Body(..., embed=True),
validate_token: str = Header("")
        # current_user: dict = Depends(get_current_user),request : Request = None
):
    # wrong_get_error = HTTPException(
    #     status_code=HTTP_400_BAD_REQUEST,
    #     detail=strings.INCORRECT_INPUT,
    # )
    try:
        encoded_body = jsonable_encoder(body)
        resp = director.signUp(encoded_body, directordb)
        return JSONResponse(status_code=resp[0], content=resp[1])
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

@router.get("/get")
async def get():
    try:
        resp = list(directordb.getModel().find())
        return JSONResponse(status_code=200,content=resp)
    except Exception as e:
        return JSONResponse(status_code=400,content={"message" : str(e)})

