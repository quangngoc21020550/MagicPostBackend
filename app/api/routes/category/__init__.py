from fastapi import APIRouter
from . import customer, director, employee, gatheringPoint, manager, packageInformation, \
            storage, toStorageOrder, toCustomerOrder, transactionPoint, userInformation
router = APIRouter()



router.include_router(customer.router, tags=["customer"], prefix='/customer')
router.include_router(director.router, tags=["director"], prefix='/director')
router.include_router(employee.router, tags=["employee"], prefix='/employee')
router.include_router(gatheringPoint.router, tags=["gatheringPoint"], prefix='/gatheringPoint')
router.include_router(manager.router, tags=["manager"], prefix='/manager')
router.include_router(packageInformation.router, tags=["packageInformation"], prefix='/packageInformation')
router.include_router(storage.router, tags=["storage"], prefix='/storage')
router.include_router(toStorageOrder.router, tags=["toStorageOrder"], prefix='/toStorageOrder')
router.include_router(toCustomerOrder.router, tags=["toCustomerOrder"], prefix='/toCustomerOrder')
router.include_router(transactionPoint.router, tags=["transactionPoint"], prefix='/transactionPoint')
router.include_router(userInformation.router, tags=["userInformation"], prefix='/userInformation')