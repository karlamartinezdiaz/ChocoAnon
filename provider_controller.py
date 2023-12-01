import os
import json
from datetime import datetime, timedelta
from database import *


class ProviderControl:
    def __init__(self):
        # Initialize with file paths for the provider directory and service records
        self.providerDirectory = 'database\provider_directory.json'

    def giveAuthorization(self, providerId):
        """
        Verifies the provider ID.
        Checks if the provider ID is exactly 9 digits.
        Returns True if valid, False otherwise.
        """
        return checkProviderID(providerId)

    def messageMemberId(self, memberId):
        """
        Checks the status of member ID and returns a status message.
        Possible return statuses are "Valid", "Invalid", and "Suspended".
        """
        return checkMemberID(memberId)

    def logout(self):
        """
        Resets the provider ID, effectively logging out the provider.
        Returns -1 to indicate the provider is logged out.
        """
        return -1

    def getProviderDirectory(self):
        """
        Retrieves the provider directory from a JSON file.
        Returns a list of service details.
        """
        return getJSONListOfDicts(self.providerDirectory)

    def verifyServiceFee(self, serviceFee, serviceCode):
        """
        Verifies if the provided service fee matches the service code.
        Returns True if the fee is correct, False otherwise.
        int(service['code']) == int(serviceCode)
        """
        if not checkServiceCode(serviceCode):
            return False
        providerDirectory = getJSONListOfDicts(self.providerDirectory)
        for service in providerDirectory:
            if int(service['code']) == serviceCode and int(service['fee']) == serviceFee:
                return True
        # print("Service Fee Not Found for Code:", serviceCode)  # Debug print I think this function is not working properly
        return False

    def verifyServiceCode(self, serviceCode):
        """
        Verifies if the provided service fee matches the service code.
        Returns True if the service code is valid, False otherwise.

        """
        try:
            providerDirectory = getJSONListOfDicts(self.providerDirectory)
            # Convert serviceCode to integer for comparison
            serviceCode = int(serviceCode)
            # Check if any service in the directory matches the provided service code
            return any(service['code'] == serviceCode for service in providerDirectory)
        except ValueError:
            # If SeerviceCode is not an integer, return False
            return False
        except Exception as e:
            # Handle other exceptions such as file not found or JSON errors
            return False

    def createServiceRecord(self, providerId, memberId, serviceCode, dateOfService, comments):
        """
        Creates a service record object with the provided details.
        The function then returns this object so it can be appended to the service records file by the terminal.
        """
        if self.giveAuthorization(providerId) and self.messageMemberId(memberId) == "Valid":
            serviceFee = self.getServiceFee(serviceCode)
            if serviceFee and self.verifyServiceFee(serviceFee, serviceCode):
                currentDatetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                currentDate, currentTime = currentDatetime.split(' ')
                serviceRecord = {
                    "current": {
                        "date": currentDate,
                        "time": currentTime
                    },
                    "date": dateOfService,
                    "providerId": providerId,
                    "memberId": memberId,
                    "serviceCode": serviceCode,
                    "comments": comments
                }

                # # Debug print statements
                # print("Service Record Created:", serviceRecord)

                # Return the service record object as a dictionary
                return serviceRecord
            else:
                return {"error": "Service fee verification failed."}
        else:
            return {"error": "Provider or Member ID is invalid."}

    def getServiceFee(self, serviceCode):
        """
        Retrieves the service fee for a given service code from the provider directory.
        Returns the service fee if found, None otherwise.
        """
        providerDirectory = getJSONListOfDicts(self.providerDirectory)
        for service in providerDirectory:
            if service['code'] == serviceCode:
                return service['fee']
        return None

    def appendServiceRecord(self, serviceRecord):
        """
        Appends a service record to the appropriate weekly service records database file,
        named by the week number of the year.
        """
        try:
            # Extract the date from the service record and parse it
            dateOfService = datetime.strptime(
                serviceRecord['date'], '%m-%d-%Y')

            # Determine the week number for the service date
            weekNumber = dateOfService.isocalendar()[1]

            # Construct the file name based on the week number of the year
            weeklyFileName = f'week_{weekNumber}.json'

            # Define the base path for the service records directory
            serviceRecordsBasePath = 'database/service_records'

            # Construct the full file path
            filePath = os.path.join(serviceRecordsBasePath, weeklyFileName)

            # Load the existing records from the file if it exists, else create a new list
            if os.path.exists(filePath):
                with open(filePath, 'r') as file:
                    serviceRecords = json.load(file)
            else:
                serviceRecords = []

            # Append the new record
            serviceRecords.append(serviceRecord)

            # Save the updated list back to the file
            with open(filePath, 'w') as file:
                json.dump(serviceRecords, file)
        except Exception as e:
            print(f"An error occurred while appending the service record: {e}")
            raise
