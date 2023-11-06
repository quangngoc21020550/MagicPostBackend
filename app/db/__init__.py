import pymongo
# from pymongo.server_api import ServerApi

from app.config import MONGO_DB_NAME, MONGO_DB_URL
# import dnspython
print(MONGO_DB_NAME)
print(MONGO_DB_URL)

client = pymongo.MongoClient(MONGO_DB_URL)
# client = pymongo.MongoClient(MONGO_DB_URL, server_api=pymongo.ServerApi('1'))
db = client[MONGO_DB_NAME]


# if not db['counters'].count() > 0:
#     db['counters'].insert_many(
#         [{"_id" : "apiapplist",
#     "sequence_value" : 0
# },
# {
#     "_id" : "apiservicelist",
#     "sequence_value" : 0
# },
# {
#     "_id" : "apiservicerouting",
#     "sequence_value" : 0
# },
# {
#     "_id" : "apisourcelist",
#     "sequence_value" : 0
# }])