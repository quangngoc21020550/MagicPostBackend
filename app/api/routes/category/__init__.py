from fastapi import APIRouter
from . import customer, director, employee, gatheringPoint, manager, packageInformation, \
            storage, toStorageOrder, toCustomerOrder, transactionPoint, userInformation, passwordForgotRequest
router = APIRouter()



router.include_router(customer.router, tags=["customer"], prefix='/customer')
router.include_router(director.router, tags=["director"], prefix='/director')
router.include_router(employee.router, tags=["employee"], prefix='/employee')
router.include_router(gatheringPoint.router, tags=["gatheringPoint"], prefix='/gathering-point')
router.include_router(manager.router, tags=["manager"], prefix='/manager')
router.include_router(packageInformation.router, tags=["packageInformation"], prefix='/package-information')
router.include_router(storage.router, tags=["storage"], prefix='/storage')
router.include_router(toStorageOrder.router, tags=["toStorageOrder"], prefix='/to-storage-order')
router.include_router(toCustomerOrder.router, tags=["toCustomerOrder"], prefix='/to-customer-order')
router.include_router(transactionPoint.router, tags=["transactionPoint"], prefix='/transaction-point')
router.include_router(userInformation.router, tags=["userInformation"], prefix='/user-information')
router.include_router(passwordForgotRequest.router, tags=['passwordForgotRequest'], prefix='/password-forgot-request')