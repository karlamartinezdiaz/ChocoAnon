# This file contains functions that interact with files in the database

import json


provRegPath = "database/provider_registry.json"
provDirPath = "database/provider_directory.json"
memRegPath = "database/member_registry.json"


# this function will create a file consisting of a single JSON object at a given path.
# If a file exists there, it will overwrite that file
# If pathname is not a string or dictionary is not a dict, will raise a TypeError
# if unable to create the file, raises an IOError
def createJSONFile(pathname, dictionary):
    try:
        if (type(pathname) != str or type(dictionary) != dict):
            raise TypeError
        with open(pathname, "w") as file:
            json.dump(dictionary, file)
            file.close()
    except IOError:
        print("ERROR: couldn't create file")
        raise
    except TypeError:
        print("ERROR: pathname or dictionary are invalid types")
        raise


# this function will create a file consisting of a list of JSON objects at a given path
# if a file exists there, it will overwrite that file
# If pathname is not a string or listOfDicts is not a list of dicts, will raise a TypeError
# if unable to create the file, raises an IOError
def createJSONListFile(pathname, listOfDicts):
    try:
        if (type(pathname) != str or type(listOfDicts) != list):
            raise TypeError
        for item in listOfDicts:
            if type(item) != dict:
                raise TypeError
        with open(pathname, "w") as file:
            json.dump(listOfDicts, file)
            file.close()
    except IOError:
        print("ERROR: couldn't create file")
        raise
    except TypeError:
        print("ERROR: pathname or listOfDicts is invalid type")
        raise


# this function will return a dictionary from a JSON file located at pathname.
# if the file is not found, raises an IOError. If the file is not a .json dict, raises a ValueError
def getJSONDict(pathname):
    try:
        with open(pathname, "r") as file:
            dictionary = json.load(file)
            print(type(dictionary))
            file.close()
        if (type(dictionary) != dict):
            raise ValueError
        return dictionary
    except IOError:
        print("ERROR: file not found")
        raise
    except ValueError:
        print("ERROR: file is not a valid .json dictionary")
        raise


# this function will return a list of dictionaries from a JSON list file located at pathname
# if the file is not found, raises an IOError. If the file is not a .json list of dicts, raises a ValueError
def getJSONListOfDicts(pathname):
    try:
        with open(pathname, "r") as file:
            listOfDicts = json.load(file)
            print(type(listOfDicts))
            file.close()
        if (type(listOfDicts) != list):
            raise ValueError
        return listOfDicts

    except IOError:
        print("ERROR: file not found")
        raise
    except ValueError:
        print("ERROR: file is not a valid .json list")
        raise


# this function checks if a provider ID is valid, returning true or false depending
def checkProviderID(ID):
    with open(provRegPath, "r") as file:
        providerList = json.load(file)
        file.close()
        for provider in providerList:
            if int(provider['Id']) == int(ID):
                return True
        return False


# this function checks if a member ID is valid, returning the status of that member if they exist, or "Invalid" if the ID is invalid
def checkMemberID(ID):
    with open(memRegPath, "r") as file:
        memberList = json.load(file)
        file.close()
        for member in memberList:
            if int(member['Id']) == int(ID):
                return member['status']
        return "Invalid"


# this function checks if a given service code is valid, returning the true or false depending
def checkServiceCode(serviceCode):
    with open(provDirPath, "r") as file:
        provDir = json.load(file)
        file.close()
        for service in provDir:
            if int(service['code']) == int(serviceCode):
                return True
        return False



# this function adds a dict that represents the member to the member registry file. If the dict is not a valid member
# dict, it raises a TypeError. If a member with that ID already exists in the database, then it raises a ValueError
def addMember(memberDict):
    try:
        if type(memberDict) != dict:
            raise TypeError
        memberList = getJSONListOfDicts(memRegPath)
        for member in memberList:
            if member['Id'] == memberDict['Id']:
                raise ValueError
        memberList.append(memberDict)
        createJSONListFile(memRegPath, memberList)

    except ValueError:
        print("ERROR: a member with that ID already exists in the registry")
        raise
    except TypeError:
        print("ERROR: invalid member dictionary")
        raise


# this function adds a dict that represents a provider to the provider registry file. If the dict is not a valid provider dict,
# it raises a TypeError. If a provider with that ID already exists in the database, then it raises a ValueError
def addProvider(providerDict):
    try:
        if type(providerDict) != dict:
            raise TypeError
        providerList = getJSONListOfDicts(provRegPath)
        for provider in providerList:
            if provider['Id'] == providerDict['Id']:
                raise ValueError
        providerList.append(providerDict)
        createJSONListFile(provRegPath, providerList)

    except ValueError:
        print("ERROR: a provider with that ID already exists in the registry")
        raise
    except TypeError:
        print("ERROR: invalid provider dictionary")
        raise


# this function deletes a member from the member registration file. It takes a valid member ID, and gives a ValueError if the ID is invalid
# raises a TypeError if the ID is not an int
def deleteMember(ID):
    try:
        if type(ID) != int:
            raise TypeError
        memberList = getJSONListOfDicts(memRegPath)
        flag = False  # used to indicate if there were any matching members in the registry or not
        for member in memberList:
            if member['Id'] == ID:
                memberList.remove(member)
                flag = True
                break
        if flag == False:
            raise ValueError
        createJSONListFile(memRegPath, memberList)

    except TypeError:
        print("ERROR: ID is not an int")
        raise
    except ValueError:
        print("ERROR: Invalid member ID")
        raise



# this function deletes a provider from the provider registration file. It takes a valid provider ID, and gives a ValueError if
# the ID in invalid. Raises a TypeError if the ID in not an int
def deleteProvider(ID):
    try:
        if type(ID) != int:
            raise TypeError
        provList = getJSONListOfDicts(provRegPath)
        flag = False  # used to indicate if there was a matching provider in the registry file
        for provider in provList:
            if provider['Id'] == ID:
                provList.remove(provider)
                flag = True
                break
        if flag == False:
            raise ValueError
        createJSONListFile(provRegPath, provList)

    except TypeError:
        print("ERROR: ID is not an int")
        raise
    except ValueError:
        print("ERROR: Invalid provider ID")
        raise
