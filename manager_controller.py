from data import *
from datetime import datetime
import database as db
import os

reportDirectory = "database/reports"
serviceDirectory = "database/service_records"


class ManagerControl:
    def __init__(self):
        pass

    def makeDict(self, dataObj):
        dataDict = dict(name=dataObj.name, Id=dataObj.Id, address=dataObj.address,
                        city=dataObj.city, state=dataObj.state, zipcode=dataObj.zipcode)
        return dataDict

    def addProvider(self, providerObj):
        providerDict = self.makeDict(providerObj)
        try:
            db.addProvider(providerDict)
            return "Provider Successfully Added"
        except Exception as e:
            return e

    # this obj will have things like name, number etc..

    def addMember(self, memberObj):
        memberDict = self.makeDict(memberObj)
        try:
            db.addMember(memberDict)
            return "Member Successfully Added"
        except Exception as e:
            return e

    def editMember(self, memberId, memberObj):
        memDict = self.makeDict(memberObj)
        try:
            db.deleteMember(memberId)
            db.addMember(memDict)
            return "Member Information Updated"
        except Exception as e:
            return e

    def editProvider(self, providerId, providerObj):
        provDict = self.makeDict(providerObj)
        try:
            db.deleteProvider(providerId)
            db.addProvider(provDict)
            return "Provider Information Updated"
        except Exception as e:
            return e

    def removeProvider(self, providerId):
        try:
            db.deleteProvider(providerId)
            return "Provider Deleted"
        except Exception as e:
            return e

    def removeMember(self, memberId):
        try:
            db.deleteMember(memberId)
            return "Member Deleted"
        except Exception as e:
            return e

    def getServiceName(self, serviceCode):
        providerDirectory = db.getJSONListOfDicts(db.provDirPath)
        for dic in providerDirectory:
            if dic['code'] == serviceCode:
                return dic['name']
        return None

    def getProviderName(self, providerId):
        providerReg = db.getJSONListOfDicts(db.provRegPath)
        for dic in providerReg:
            if dic['Id'] == providerId:
                return dic['name']
        return None

    def getRecentWeek(self):
        files = []
        for file in os.listdir(serviceDirectory):
            fullPath = os.path.join(serviceDirectory, file)
            if os.path.isfile(fullPath):
                files.append(fullPath)
            if not files:
                return None
        return files[-1]

    def getMemberService(self, servicePath,  memberId):
        serviceRecord = db.getJSONListOfDicts(servicePath)
        serviceList = []
        dateOfService = ""
        providerName = ""
        serviceName = " "
        for dic in serviceRecord:
            if dic['memberId'] == memberId:
                dateOfService = dic['dateOfService']
                providerName = self.getProviderName(dic['providerId'])
                serviceName = self.getServiceName(dic['serviceCode'])
                serviceList.append(
                    {"date": dateOfService, "providerName": providerName, "serviceName": serviceName})
        return serviceList

    def createMemberReport(self):
        servicePath = self.getRecentWeek()
        weekName = servicePath[25:]
        memRegList = db.getJSONListOfDicts(db.memRegPath)
        memberDirectoryPath = ''
        providersDirectoryPath = ''
        for memdic in memRegList:
            serviceList = self.getMemberService(servicePath, memdic['Id'])
            memdic['services'] = serviceList
            memberDirectoryPath, providersDirectoryPath = self.createWeekDirectories()
            self.addMemDict(memdic, weekName, memberDirectoryPath)

    def createWeekDirectories(self):
        memberDirectoryPath = ' '
        providersDirectoryPath = ' '
        for fileName in os.listdir(serviceDirectory):
            if fileName.endswith('.json'):
                directoryName = fileName[:-5]
                newDirectoryPath = os.path.join(reportDirectory, directoryName)
                if not os.path.exists(newDirectoryPath):
                    memberDirectoryPath = os.path.join(
                        newDirectoryPath, "members")
                    providersDirectoryPath = os.path.join(
                        newDirectoryPath, "providers")
                    os.makedirs(newDirectoryPath)
                    os.makedirs(memberDirectoryPath)
                    os.makedirs(providersDirectoryPath)
                else:
                    memberDirectoryPath = os.path.join(
                        newDirectoryPath, "members")
                    providersDirectoryPath = os.path.join(
                        newDirectoryPath, "providers")
        return memberDirectoryPath, providersDirectoryPath

    def addMemDict(self, memObject, weekName, memberDirectoryPath):
        if os.path.exists(memberDirectoryPath):
            memberFileName = memObject['name'] + '_' + weekName
            newMemberPathName = os.path.join(
                memberDirectoryPath, memberFileName)
            db.createJSONFile(newMemberPathName, memObject)

    def viewMemberReport(memberFile):
        return database.memberReport(memberId)

    def viewProviderReport(providerFile):
        return database.providerReport(providerId)


manager = ManagerControl()
manager.getMemberDict()
