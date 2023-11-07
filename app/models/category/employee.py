import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from app.models.modelbase import modelBase


class employeeModel(BaseModel):
    id: str = Field(..., alias='_id')
    username: str
    type: str
    # info ....
    managedBy: str
    createdDate: int
    lastUpdatedDate: int

class employeeDel(BaseModel):
    id: str = Field(..., alias='_id')

class employeeSearch(BaseModel):
    content : dict
    pagesize: int
    pageindex: int

class employeeInsmodel(BaseModel):
    username: str
    type: str
    # info ....
    managedBy: str
    createdDate: int
    lastUpdatedDate: int


class employee(modelBase):
    pass
