import unittest
from provider_controller import ProviderControl
from database import checkProviderID, checkMemberID


class TestProviderControl(unittest.TestCase):
    def setUp(self):
        # Initialize a ProviderControl instance for testing
        self.provider_control = ProviderControl()

    # authenticataion tests-----------------------------------------------
    def test_giveAuthorization_valid(self):
        # Test giveAuthorization with a valid provider ID
        provider_id = "111333111"
        result = self.provider_control.giveAuthorization(provider_id)
        db_result = checkProviderID(provider_id)
        self.assertTrue(result)
        self.assertTrue(db_result)

    def test_giveAuthorization_invalid(self):
        # Test giveAuthorization with an invalid provider ID
        invalid_provider_id = "222222221"  # this doesnt exist in the database
        result = self.provider_control.giveAuthorization(invalid_provider_id)
        db_result = checkProviderID(invalid_provider_id)
        self.assertFalse(result)
        self.assertFalse(db_result)

    # Member ID validation tests-----------------------------------------------
    def test_messageMemberId_valid(self):
        # Test messageMemberId with a valid member ID
        member_id = "987654321"
        result = self.provider_control.messageMemberId(member_id)
        db_result = checkMemberID(member_id)
        self.assertEqual(result, "Valid")
        self.assertEqual(db_result, "Valid")

    def test_messageMemberId_invalid(self):
        # Test messageMemberId with an invalid member ID
        invalid_member_id = "987654322"  # this doesnt exist in the database
        result = self.provider_control.messageMemberId(invalid_member_id)
        db_result = checkMemberID(invalid_member_id)
        self.assertEqual(result, "Invalid")
        self.assertEqual(db_result, "Invalid")

    def test_messageMemberId_valid(self):
        # Test messageMemberId with a valid member ID
        valid_member_id = "111333111"  # valid member ID from  database
        result = self.provider_control.messageMemberId(valid_member_id)
        self.assertEqual(result, "Valid")

    def test_messageMemberId_invalid(self):
        # Test messageMemberId with an Invalid member ID
        # Use an invalid member ID that doesn't exist in  database
        invalid_member_id = "987654322"
        result = self.provider_control.messageMemberId(invalid_member_id)
        self.assertEqual(result, "Invalid")

    def test_messageMemberId_suspended(self):
        # test messageMemberId with a suspended Member ID (customize this based on data)
        suspended_member_id = "396352333"  # suspended member ID from  database
        result = self.provider_control.messageMemberId(suspended_member_id)
        self.assertEqual(result, "Suspended")

        # Logout tests-----------------------------------------------
    def test_logout(self):
        # Test logou functionality
        result = self.provider_control.logout()
        self.assertEqual(result, -1)  # Assuming -1 is logged-out state

    # Provider Directory tests-----------------------------------------------
    def test_getProviderDirectory(self):
        # Test retrieval of provider directory
        directory = self.provider_control.getProviderDirectory()
        # Assuming it should return a list
        self.assertIsInstance(directory, list)
        # Assuming the directory is not empty
        self.assertGreater(len(directory), 0)

    # Service Fee Verification tests-----------------------------------------------
    def test_verifyServiceFee_valid(self):
        # Test verifyServiceFee with valid inputs
        valid_service_fee = 150  # valid service fee from database
        valid_service_code = 123456  # valid service code from database
        result = self.provider_control.verifyServiceFee(
            valid_service_fee, valid_service_code)
        self.assertTrue(result)

    def test_verifyServiceFee_invalid(self):
        # Test verifyServiceFee with invalid inputs
        invalid_service_fee = 20  # invalid service fee that doesn't match any service code
        invalid_service_code = 190  # invalid service code that doesn't exist
        result = self.provider_control.verifyServiceFee(
            invalid_service_fee, invalid_service_code)
        self.assertFalse(result)

    # Get Service Fee tests-----------------------------------------------
    def test_getServiceFee_valid(self):
        # Test getServiceFee with a valid service code
        valid_service_code = 123456  # alid service code from Database
        fee = self.provider_control.getServiceFee(valid_service_code)
        # Assuming there is a fee for this service code
        self.assertIsNotNone(fee)
        # Assuming 150 is the correct fee for this service
        self.assertEqual(fee, 150)

    def test_getServiceFee_invalid(self):
        # Test getServiceFee with an invalid service code
        invalid_service_code = 654321  # Use an invalid service code that doesn't exist
        fee = self.provider_control.getServiceFee(invalid_service_code)
        # Assuming there is no fee for this service code
        self.assertIsNone(fee)

    # Verify Service Code tests-----------------------------------------------
    def test_verifyServiceCode_valid(self):
        # Test verifyServiceCode with a valid service code
        valid_service_code = 123456  # Valid service code from database
        result = self.provider_control.verifyServiceCode(valid_service_code)
        self.assertTrue(result)

    def test_verifyServiceCode_invalid(self):
        # Test verifyServiceCode with an invalid service code
        invalid_service_code = 654321  # invalid service code that doesn't exist
        result = self.provider_control.verifyServiceCode(invalid_service_code)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
