# Danh sách các API publish ra
# product
#   {
#   _id : String (sinh mã - số tự tăng - Để dễ nhớ)
#   code: String (sinh mã - nếu có trường id thì ko cần trường này)
#   method: String
#   url: String
#   headerList: ListObject[{"key": String, "value": String}]
#   bodySchema: String - Dùng trong trường hợp khi cần validate dữ liệu truyền vào
#   isActive: Boolean
#   status: Number
#   info:{} - Sử dụng để thêm thông tin sau này khi cần
#   }

import pymongo
from typing import Optional
from pydantic import BaseModel, HttpUrl,Field,AnyUrl
from uuid import UUID
from typing import List,Dict
from pydantic import IPvAnyAddress
from app.models.modelbase import modelBase


class productModel(BaseModel):
    id: str = Field(..., alias='_id')
    name: str
    price: int = 0

class productDel(BaseModel):
    id: str = Field(..., alias='_id')

class productSearch(BaseModel):
    content : Dict
    pagesize: int
    pageindex: int

class productInsmodel(BaseModel):
    name: str
    price: int = 0


class product(modelBase):
    pass
