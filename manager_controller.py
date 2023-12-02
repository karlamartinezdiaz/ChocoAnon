from data import *
from datetime import datetime
import database as db
import os

reportDirectory = "database/reports"
serviceDirectory = "database/service_records"


class ManagerControl:
    def __init__(self):
        pass

    # Converts data object into a dictionary
    def makeDict(self, dataObj):
        dataDict = dict(name=dataObj.name, Id=dataObj.Id, address=dataObj.address,
                        city=dataObj.city, state=dataObj.state, zipcode=dataObj.zipcode)
        return dataDict

    
    # Adds a new provider to the database
    def addProvider(self, providerObj):
        providerDict = self.makeDict(providerObj)
        try:
            db.addProvider(providerDict)
            return "Provider Successfully Added"
        except Exception as e:
            return e

    # Adds a new member to the database
    def addMember(self, memberObj):
        memberDict = self.makeDict(memberObj)
        try:
            db.addMember(memberDict)
            return "Member Successfully Added"
        except Exception as e:
            return e

    # Edits an existing member's information in the database.
    # First deletes the old record and then adds the updated one
    def editMember(self, memberId, memberObj):
        memDict = self.makeDict(memberObj)
        try:
            db.deleteMember(memberId)
            db.addMember(memDict)
            return "Member Information Updated"
        except Exception as e:
            return e

    # Edits an existing provider's information in the database.
    # First deletes the old record and then adds the updated one
    def editProvider(self, providerId, providerObj):
        provDict = self.makeDict(providerObj)
        try:
            db.deleteProvider(providerId)
            db.addProvider(provDict)
            return "Provider Information Updated"
        except Exception as e:
            return e

    # Removes the provider from that database using their Id
    def removeProvider(self, providerId):
        try:
            db.deleteProvider(providerId)
            return "Provider Deleted"
        except Exception as e:
            return e

    # Removes the member from that database using their Id
    def removeMember(self, memberId):
        try:
            db.deleteMember(memberId)
            return "Member Deleted"
        except Exception as e:
            return e

    # Retrieves specific information about a service based on its code.
    def getServiceInfo(self, serviceCode, info):
        providerDirectory = db.getJSONListOfDicts(db.provDirPath)
        for dic in providerDirectory:
            if dic['code'] == serviceCode:
                return dic[info]
        return None

    # Retrives the name of a provider using their Id
    def getProviderName(self, providerId):
        providerReg = db.getJSONListOfDicts(db.provRegPath)
        for dic in providerReg:
            if dic['Id'] == providerId:
                return dic['name']
        return None

    # Retrives the name of a member using their Id
    def getMemberName(self, memberId):
        memberReg = db.getJSONListOfDicts(db.memRegPath)
        for dic in memberReg:
            if dic['Id'] == memberId:
                return dic['name']
        return None

    # Retrieves the most recent service record based on file dates in a directory.
    def getRecentWeek(self):
        files = []
        for file in os.listdir(serviceDirectory):
            fullPath = os.path.join(serviceDirectory, file)
            if os.path.isfile(fullPath):
                files.append(fullPath)
            if not files:
                return None
        return files[-1]

    # Calculates the total fee for a list of services
    def getTotalFee(self, serviceList):
        fee = 0
        for service in serviceList:
            fee += service['fee']
        return fee

    # Retrives a list of services for a particular member
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
                serviceName = self.getServiceInfo(dic['serviceCode'], "name")
                serviceList.append(
                    {"date": dateOfService, "providerName": providerName, "serviceName": serviceName})
        return serviceList

    # Retrives a list of services provided by a particular provider
    def getProviderService(self, servicePath, providerId):
        serviceRecord = db.getJSONListOfDicts(servicePath)
        serviceList = []
        for dic in serviceRecord:
            if dic['providerId'] == providerId:
                memberName = self.getMemberName(dic['memberId'])
                fee = self.getServiceInfo(dic['serviceCode'], 'fee')
                dic['memberName'] = memberName
                dic['fee'] = fee
                dic.pop('comments')
                dic.pop('providerId')
                serviceList.append(dic)
        return serviceList

    # Generates a comprehensive report for the most recent week.
    # It includes member and provider service details, along with Electronic Transfer Fund (ETF) information.
    def createReport(self):
        servicePath = self.getRecentWeek()
        weekName = servicePath[25:]
        memRegList = db.getJSONListOfDicts(db.memRegPath)
        provRegList = db.getJSONListOfDicts(db.provRegPath)
        etfList = []
        memberDirectoryPath = ''
        providersDirectoryPath = ''
        etfDirectoryPath = ''

        # Loops through each member, retrieves their service details, and adds them to the member directory.
        for memdic in memRegList:
            serviceList = self.getMemberService(servicePath, memdic['Id'])
            if serviceList:
                memdic['services'] = serviceList
                memdic.pop('status')
                memberDirectoryPath, providersDirectoryPath, etfDirectoryPath = self.createWeekDirectories()
                self.addMemDict(memdic, weekName, memberDirectoryPath)
        for provdic in provRegList:
            serviceList = self.getProviderService(servicePath, provdic['Id'])
            if serviceList:
                provdic['services'] = serviceList
                provdic['totalConsults'] = len(serviceList)
                provdic['totalFee'] = self.getTotalFee(serviceList)
                provdic.pop('status')
                self.addProvDict(provdic, weekName, providersDirectoryPath)
                etfDic = {
                    'providerName': provdic['name'], 'providerId': provdic['Id'], 'amountToTransfer': provdic['totalFee']}
                etfList.append(etfDic)
        db.createJSONListFile(etfDirectoryPath, etfList)

    # Creates new directories for storing weekly reports, including separate directories for members and providers.
    def createWeekDirectories(self):
        memberDirectoryPath = ' '
        providersDirectoryPath = ' '
        newDirectoryPath = ' '
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
        etfDirectoryPath = os.path.join(newDirectoryPath, "etf.json")
        return memberDirectoryPath, providersDirectoryPath, etfDirectoryPath

     # Adds a member's information as a JSON file in the member directory for the specified week.
    def addMemDict(self, memObject, weekName, memberDirectoryPath):
        if os.path.exists(memberDirectoryPath):
            memberFileName = memObject['name'] + '_' + weekName
            newMemberPathName = os.path.join(
                memberDirectoryPath, memberFileName)
            db.createJSONFile(newMemberPathName, memObject)

    # Adds a provider's information as a JSON file in the provider directory for the specified week.

    def addProvDict(self, provObject, weekName, providersDirectoryPath):
        if os.path.exists(providersDirectoryPath):
            providerFileName = provObject['name'] + '_' + weekName
            newProviderPathName = os.path.join(
                providersDirectoryPath, providerFileName)
            db.createJSONFile(newProviderPathName, provObject)

