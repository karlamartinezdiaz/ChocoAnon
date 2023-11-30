import datetime
from database import *


class ProviderControl:
    def __init__(self):
        # Initialize with file paths for the provider directory and service records
        self.providerDirectory = 'database\provider_directory.json'
        # Ensure this path is correct

    def giveAuthorization(self, providerId):
        """
        Verifies the provider ID.
        Checks if the provider ID is exactly 9 digits.
        Returns True if valid, False otherwise.
        """
        if len(providerId) != 9 or not providerId.isdigit():
            return False
        return checkProviderID(providerId)

    def messageMemberId(self, memberId):
        """
        Checks the status of member ID and returns a status message.
        Possible return statuses are "Valid", "Invalid", and "Suspended".
        """
        if len(memberId) != 9 or not memberId.isdigit():
            return "Invalid"  # Member ID must be a 9-digit number
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
                current_datetime = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                current_date, current_time = current_datetime.split(' ')
                service_record = {
                    "current": {
                        "date": current_date,
                        "time": current_time
                    },
                    "date": dateOfService,
                    "provider_ID": providerId,
                    "member_ID": memberId,
                    "service_code": serviceCode,
                    "comments": comments
                }
                # Return the service record object to the terminal/caller
                return service_record
            else:
                return None, "Service fee verification failed."
        else:
            return None, "Provider or Member ID is invalid."

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
