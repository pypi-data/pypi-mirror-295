import json

class Create:
    def __init__(self):
        self.json = {}

    def addJsonArray(self,key,value):
        self.json[key] = [value]

    def addJsonObject(self, key, value):
        self.json[key] = value

    def getData(self):
        return self.json

    def getJson(self):
        return json.dumps(self.json)
