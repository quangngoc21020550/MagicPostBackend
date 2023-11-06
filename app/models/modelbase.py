# {
#     _id: String
#     appname: string
#     host: String
#     port: String
#     status: number
#     info: {} - Sử dụng để thêm thông tin sau này khi cần
# }


import pymongo
import jsonschema
from jsonschema import validate
import json
import uuid
# from app.callcache import dict_cache



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

    def search(self,*args,**kwargs):
        try:

            request_json = kwargs.get("json")
            print(request_json)

            content = request_json.get('content') if request_json.get('content') else None
            page = int(request_json.get('pageindex')) if 'pageindex' in request_json.keys() else None
            pagesize = int(request_json.get('pagesize')) if 'pagesize' in request_json.keys() else None

            if not (self.schemasearch == None or self.schemasearch == "") and self.validateJson(content,self.schemasearch):
                return (400,"JsonSchema failed validation")


            if (not page or page ==0): page=1
            if (not pagesize or page ==0): pagesize=10



            channelCrs = None
            if content != None and content != {}:
                for k, v in list(content.items()):
                    if v == None:
                        content.pop(k)

                channelCrs = self.db[self.clname].find(content).limit(pagesize).skip((page-1)*pagesize)
            else:
                # print("2")


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

            try:
                idss = request_json['_id']
            except:
                idss = str(uuid.uuid4())
                request_json['_id'] = idss

            # print(idss)

            request_json['_id'] = idss
            docinserted = self.db[self.clname].insert(request_json)
            if docinserted == idss:
                it = self.db[self.clname].find_one({'_id':docinserted})
                # dict_cache.runApp()

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
                # dict_cache.runApp()
                return (200, {"_id":id})
            else:
                return (400, {"_id": None})
            # print(docdeleted.deleted_count)

        except Exception as e:
            return (400,str(e))


    def update_doc(self,*args,**kwargs):


        try:
            request_json = kwargs.get("json")
            if self.schema != None and self.validateJson(request_json, self.schema) == False:
                return (400, "JsonSchema failed validation")
            id = request_json['_id']
            docinserted = self.db[self.clname].update({'_id': id}, request_json, upsert=False)
            # dict_cache.runApp()
            doc = self.db[self.clname].find_one({'_id': id})
            return (200,doc)
        except Exception as e:
            return (400,str(e))



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

