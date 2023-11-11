# {
#     _id: String
#     appname: string
#     host: String
#     port: String
#     status: number
#     info: {} - Sử dụng để thêm thông tin sau này khi cần
# }


import traceback
import uuid

import jsonschema
import pymongo
from jsonschema import validate
from pymongo import UpdateOne
import time


class modelBase:
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs
        self.clname = kwargs.get("collectionname")
        self.db = kwargs.get("db")
        self.schema = kwargs.get("schema") if kwargs.get('schema') else None
        self.schemasearch = kwargs.get("schemasearch") if kwargs.get('schemasearch') else None


    def getModel(self):
        return self.db[self.clname]

    # mongo.db.get_collection



    def search(self,*args,**kwargs):
        try:

            request_json = kwargs.get("json")
            print(request_json)

            content = request_json.get('content') if request_json.get('content') else None
            page = int(request_json.get('pageindex')) if 'pageindex' in request_json.keys() else None
            pagesize = int(request_json.get('pagesize')) if 'pagesize' in request_json.keys() else None
            searchnone = kwargs.get("searchnone") if 'searchnone' in kwargs.keys() else False

            if not (self.schemasearch == None or self.schemasearch == "") and self.validateJson(content,self.schemasearch):
                return (400,"JsonSchema failed validation")


            if (not page or page ==0): page=1
            if (not pagesize or page ==0): pagesize=100000



            channelCrs = None
            if content != None and content != {}:
                if searchnone == False:
                    for k, v in list(content.items()):
                        if v == None:
                            content.pop(k)
                channelCrs = self.db[self.clname].find(content).limit(pagesize).skip((page-1)*pagesize)
            else:
                channelCrs = self.db[self.clname].find().limit(pagesize).skip((page - 1) * pagesize)

            out = []
            try:
                while True:
                    out.append(channelCrs.next())
            except StopIteration:
                # do nothing
                pass
            return (200, out)

            # return (200,uid)
        except Exception as e:
            return (400, str(e))

    def insert_doc(self,*args,**kwargs):



        # print(idss)

        try:
            request_json = kwargs.get("json")

            if self.schema != None and self.validateJson(request_json, self.schema) == False:
                return (400, "JsonSchema failed validation")

            # print(self.clname)
            if "_id" not in request_json:
                idss = str(uuid.uuid4())
            else:
                idss = request_json["_id"]
            # print(idss)

            request_json['_id'] = idss
            # if "createdate" not in request_json:
            #      request_json['createdate']= round(time.time() * 1000)
            # elif request_json["createdate"] == 0:
            #     request_json['createdate'] = round(time.time() * 1000)
            # if "updatedate" not in request_json:
            #     request_json['updatedate']= None
            # elif request_json["updatedate"] == 0:
            #     request_json['updatedate'] = None

            docinserted = self.db[self.clname].insert_one(request_json)
            if docinserted.inserted_id == idss:
                it = self.db[self.clname].find_one({'_id': idss})

                return (200,it)
            else:
                return (400,docinserted)
        except pymongo.errors.DuplicateKeyError as e:
            self.insert_doc(request_json)


    def delete_doc(self,*args,**kwargs):


        try:
            request_json = kwargs.get("json")
            id = request_json['_id']
            docdeleted = self.db[self.clname].delete_one({'_id':id})
            if docdeleted.deleted_count ==1:
                return (200, {"_id":id})
            else:
                return (200, {"_id": None})
            # print(docdeleted.deleted_count)

        except Exception as e:
            traceback.print_exc()
            return (400,str(e))


    def update_doc(self,*args,**kwargs):


        try:
            request_json = kwargs.get("json")
            id = request_json['_id']
            if self.schema != None and self.validateJson(request_json, self.schema) == False:
                return (400, "JsonSchema failed validation")
            request_json['updatedate'] = round(time.time() * 1000)

            # print(request_json)

            docinserted = self.db[self.clname].update_one({'_id': id},{"$set": request_json}, upsert=False)
            return (200,request_json)
        except Exception as e:
            return (400,str(e))

    def aggregate_search(self,*args,**kwargs):
        try:

            request_json = kwargs.get("json")

            content = request_json.get('content') if request_json.get('content') else None
            if not (self.schemasearch == None or self.schemasearch == "") and self.validateJson(content,self.schemasearch):
                return (400,"JsonSchema failed validation")

            channelCrs = self.db[self.clname].aggregate(content)


            out = []
            try:
                while True:
                    out.append(channelCrs.next())
            except StopIteration:
                # do nothing
                pass
            return (200, out)

            # return (200,uid)
        except Exception as e:
            return (400, str(e))

    def findAllData(self):
        try:
            channelCrs = self.db[self.clname].find()

            out = []
            try:
                while True:
                    out.append(channelCrs.next())
            except StopIteration:
                # do nothing
                pass
            return (200, out)

            # return (200,uid)

        except Exception as e:
            return (400, str(e))


    def validateJson(self,jsonData,schema):
        try:
            validate(instance=jsonData, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True

    def insert_many_docs(self, *args, **kwargs):

        # print(idss)

        try:
            list_request_json = list(kwargs.get("json"))

            if self.schema != None and self.validateJson(list_request_json, self.schema) == False:
                return (400, "JsonSchema failed validation")

            # print(self.clname)
            listidss= []
            for request_json in list_request_json:
                if "_id" not in request_json:
                    idss = str(uuid.uuid4())
                    listidss.append(idss)
                else:
                    idss = request_json["_id"]
                    listidss.append(idss)

                # print(idss)
                request_json['createdate'] = round(time.time() * 1000)
                request_json['updatedate'] = None
                request_json['_id'] = idss
            docinserted = self.db[self.clname].insert_many(list_request_json)
            if docinserted.inserted_ids == listidss:
                it = self.db[self.clname].find({'_id': {"$in":docinserted.inserted_ids}})
                out = []
                try:
                    while True:
                        out.append(it.next())
                except StopIteration:
                    # do nothing
                    pass
                return (200, out)
            else:
                return (400, docinserted)
        except pymongo.errors.DuplicateKeyError as e:
            self.insert_doc(request_json)
    def update_many_docs(self,*args,**kwargs):


        try:
            list_request_json = list(kwargs.get("json"))
            list_id= list(map(lambda x: x["_id"],list_request_json))
                # id = request_json['_id']
            if self.schema != None and self.validateJson(list_request_json, self.schema) == False:
                    return (400, "JsonSchema failed validation")
            updates=[]
            for item in list_request_json:
                updates.append(UpdateOne({'_id': item["_id"]}, {"$set":item}))
            docinserted = self.db[self.clname].bulk_write(updates)
            return (200,docinserted)
        except Exception as e:
            return (400,str(e))

