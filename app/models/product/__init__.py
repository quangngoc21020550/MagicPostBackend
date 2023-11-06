from . import product
from app.db import db

productdb = product.product(collectionname="product",db=db)