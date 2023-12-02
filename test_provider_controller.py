import unittest
from unittest.mock import patch, mock_open
from provider_controller import ProviderControl
from database import checkProviderID, checkMemberID


class TestProviderControl(unittest.TestCase):
    def setUp(self):
        # Initialize a ProviderControl instance for testing
        self.providerControl = ProviderControl()

    # Authentication tests-----------------------------------------------
    def test_giveAuthorization_valid(self):
        # Test giveAuthorization with a valid provider ID
        providerId = "111333112"
        result = self.providerControl.giveAuthorization(providerId)
        dbResult = checkProviderID(providerId)
        self.assertTrue(result)
        self.assertTrue(dbResult)

    def test_giveAuthorization_invalid(self):
        # Test giveAuthorization with an invalid provider ID
        invalidProviderId = "222222221"  # This doesn't exist in the database
        result = self.providerControl.giveAuthorization(invalidProviderId)
        dbResult = checkProviderID(invalidProviderId)
        self.assertFalse(result)
        self.assertFalse(dbResult)

    # Member ID validation tests-----------------------------------------------
    def test_messageMemberId_valid(self):
        # Test messageMemberId with a valid member ID
        memberId = "987654321"
        result = self.providerControl.messageMemberId(memberId)
        dbResult = checkMemberID(memberId)
        self.assertEqual(result, "Valid")
        self.assertEqual(dbResult, "Valid")

    def test_messageMemberId_invalid(self):
        # Test messageMemberId with an invalid member ID
        invalidMemberId = "987654322"  # This doesn't exist in the database
        result = self.providerControl.messageMemberId(invalidMemberId)
        dbResult = checkMemberID(invalidMemberId)
        self.assertEqual(result, "Invalid")
        self.assertEqual(dbResult, "Invalid")

    def test_messageMemberId_valid(self):
        # Test messageMemberId with a valid member ID
        validMemberId = "111333111"  # Valid member ID from the database
        result = self.providerControl.messageMemberId(validMemberId)
        self.assertEqual(result, "Valid")

    def test_messageMemberId_invalid(self):
        # Test messageMemberId with an invalid member ID
        # Use an invalid member ID that doesn't exist in the database
        invalidMemberId = "987654322"
        result = self.providerControl.messageMemberId(invalidMemberId)
        self.assertEqual(result, "Invalid")

    def test_messageMemberId_suspended(self):
        # Test messageMemberId with a suspended Member ID (customize this based on data)
        suspendedMemberId = "396352333"  # Suspended member ID from the database
        result = self.providerControl.messageMemberId(suspendedMemberId)
        self.assertEqual(result, "Suspended")

    # Logout tests-----------------------------------------------
    def test_logout(self):
        # Test logout functionality
        result = self.providerControl.logout()
        self.assertEqual(result, -1)  # Assuming -1 is logged-out state

    # Provider Directory tests-----------------------------------------------
    def test_getProviderDirectory(self):
        # Test retrieval of provider directory
        directory = self.providerControl.getProviderDirectory()
        # Assuming it should return a list
        self.assertIsInstance(directory, list)
        # Assuming the directory is not empty
        self.assertGreater(len(directory), 0)

    # Service Fee Verification tests-----------------------------------------------
    def test_verifyServiceFee_valid(self):
        # Test verifyServiceFee with valid inputs
        validServiceFee = 150  # Valid service fee from the database
        validServiceCode = 123456  # Valid service code from the database
        result = self.providerControl.verifyServiceFee(
            validServiceFee, validServiceCode)
        self.assertTrue(result)

    def test_verifyServiceFee_invalid(self):
        # Test verifyServiceFee with invalid inputs
        invalidServiceFee = 20  # Invalid service fee that doesn't match any service code
        invalidServiceCode = 190  # Invalid service code that doesn't exist
        result = self.providerControl.verifyServiceFee(
            invalidServiceFee, invalidServiceCode)
        self.assertFalse(result)

    # Get Service Fee tests-----------------------------------------------
    def test_getServiceFee_valid(self):
        # Test getServiceFee with a valid service code
        validServiceCode = 123456  # Valid service code from the database
        fee = self.providerControl.getServiceFee(validServiceCode)
        # Assuming there is a fee for this service code
        self.assertIsNotNone(fee)
        # Assuming 150 is the correct fee for this service
        self.assertEqual(fee, 150)

    def test_getServiceFee_invalid(self):
        # Test getServiceFee with an invalid service code
        invalidServiceCode = 654321  # Use an invalid service code that doesn't exist
        fee = self.providerControl.getServiceFee(invalidServiceCode)
        # Assuming there is no fee for this service code
        self.assertIsNone(fee)

    # Verify Service Code tests-----------------------------------------------
    def test_verifyServiceCode_valid(self):
        # Test verifyServiceCode with a valid service code
        validServiceCode = 123456  # Valid service code from the database
        result = self.providerControl.verifyServiceCode(validServiceCode)
        self.assertTrue(result)

    def test_verifyServiceCode_invalid(self):
        # Test verifyServiceCode with an invalid service code
        invalidServiceCode = 654321  # Invalid service code that doesn't exist
        result = self.providerControl.verifyServiceCode(invalidServiceCode)
        self.assertFalse(result)

    def test_createServiceRecord_valid(self):
        # Test creating a service record with valid inputs
        providerId = "111333112"
        memberId = "111333111"
        serviceCode = 123456  # Valid service code from the database
        dateOfService = "01-15-2023"
        comments = "Test service record"

        serviceRecord = self.providerControl.createServiceRecord(
            providerId, memberId, serviceCode, dateOfService, comments)

        # Ensure that the service record is not None
        self.assertIsNotNone(serviceRecord)

        self.providerControl.appendServiceRecord(serviceRecord)

        # Check specific attributes of the service record if needed
        # Use "providerId" key as returned by createServiceRecord
        self.assertEqual(serviceRecord["providerId"], providerId)
        self.assertEqual(serviceRecord["memberId"], memberId)
        self.assertEqual(serviceRecord["serviceCode"], serviceCode)
        self.assertEqual(serviceRecord["date"], dateOfService)
        self.assertEqual(serviceRecord["comments"], comments)

    def test_verifyService(self):
        # Testing by drawing data from a service record
        dateOfService = "01-15-2023"
        memName = "Member1"
        memId = 111333111
        serviceCode = 123456
        feePaid = 150

        result = self.providerControl.verifyService(
            dateOfService, memName, memId, serviceCode, feePaid)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
