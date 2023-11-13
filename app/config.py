

MONGO_DB_URL = 'mongodb+srv://magicpost:21020550@magicpost.uvauqpt.mongodb.net/?retryWrites=true&w=majority'
MONGO_DB_NAME = "MagicPostTest"

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

TOKEN_EXPIRED = 60 * 60 * 24 * 2   #seconds

VALID_ROLES = ['customer', 'gathering-point-manager', 'transaction-point-manager', 'gathering-point-employee', 'transaction-point-employee', 'director']