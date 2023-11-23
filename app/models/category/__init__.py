from . import customer, director, employee, gatheringPoint, manager, packageInformation, \
            storage, toStorageOrder, toCustomerOrder, transactionPoint, userInformation, passwordForgotRequest
from app.db import db

customerdb = customer.customer(collectionname="customer",db=db)
directordb = director.director(collectionname="director",db=db)
employeedb = employee.employee(collectionname="employee",db=db)
gatheringPointdb = gatheringPoint.gatheringPoint(collectionname="gatheringPoint",db=db)
managerdb = manager.manager(collectionname="manager",db=db)
packageInformationdb = packageInformation.packageInformation(collectionname="packageInformation",db=db)
storagedb = storage.storage(collectionname="storage",db=db)
toStorageOrderdb = toStorageOrder.toStorageOrder(collectionname="toStorageOrder",db=db)
toCustomerOrderdb = toCustomerOrder.toCustomerOrder(collectionname="toCustomerOrder",db=db)
transactionPointdb = transactionPoint.transactionPoint(collectionname="transactionPoint",db=db)
userInformationdb = userInformation.userInformation(collectionname="userInformation",db=db)
passwordForgotRequestdb = passwordForgotRequest.passwordForgotRequest(collectionname="passwordForgotRequest",db=db)