from fastapi import APIRouter
from . import productAPI
router = APIRouter()



router.include_router(productAPI.router, tags=["product"], prefix="/product")
# router.include_router(kidfileAPI.router, tags=["kidfile"], prefix="/filerequest")