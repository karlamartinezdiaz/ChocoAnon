import __init__
import models.database as db
from data import *
from datetime import datetime
from database import *


class ManagerControl:
    def __init__(self):
        pass

    def makeDict(self, dataObj):
        print(provDirPath)
        dataDict = dict(name=dataObj.name, Id=dataObj.Id, address=dataObj.address,
                        city=dataObj.city, state=dataObj.state, zipcode=dataObj.zipcode)
        return dataDict

    def addProvider(self, providerObj):
        providerDict = self.makeDict(providerObj)
        addProvider(providerDict)

    # this obj will have things like name, number etc..
    def addMember(self, memberObj):
        memberDict = self.makeDict(memberObj)
        addMember(memberDict)

    def editMember(self, memberId, memberObj):
        memDict = getJSONListOfDicts(memRegPath)
        for mem in memDict:
            if (mem['Id'] == memberId):
                mem.update(memberObj)
        createJSONListFile(memRegPath, memDict)

    def editProvider(self, providerId, providerObj):
        print(provRegPath)
        provDict = getJSONListOfDicts(provRegPath)
        for prov in provDict:
            if (prov['Id'] == providerId):
                prov.update(providerObj)
        createJSONListFile(provRegPath, provDict)

    def removeProvider(self, providerId):
        deleteProvider(providerId)

    def removeMember(self, memberId):
        deleteMember(memberId)

    def viewMemberReport(memberFile):
        return database.memberReport(memberId)

    def viewProviderReport(providerFile):
        return database.providerReport(providerId)


obj = {"name": "billy", "Id": 22244422, "address": "224 22nd St",
       "city": "Two Town", "state": "OR", "zipcode": 22222, "status": "Valid"}

manager = ManagerControl()
manager.removeMember(22244422)
