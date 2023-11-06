import pymongo


from app.config import MONGO_DB_NAME, MONGO_DB_URL

print(MONGO_DB_NAME)
print(MONGO_DB_URL)

client = pymongo.MongoClient(MONGO_DB_URL)
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