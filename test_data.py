from data import BasicData
from data import ServiceData

from unittest.mock import patch
import pytest


def test_BasicData():
    basic_data = BasicData("John Doe", 123456789,
                           "1234 street", "City_name", "State_name", 12345)
    assert basic_data.name == "John Doe"
    assert basic_data.city == "City_name"
    assert basic_data.state == "State_name"
    assert basic_data.address == "1234 street"
    assert basic_data.Id == 123456789
    assert basic_data.zipcode == 12345


def test_ServiceData():
    def test_ServiceData():
        with patch('builtins.input', side_effect=["12-01-2023"]):
            service_data = ServiceData(
                "02:00:00", "12-01-2023", 123456789, 987654321, 900000000, "Hay Girl")
        service_data.createServiceData()
        assert service_data.time == "12-01-2023 02:00:00"
        assert service_data.dateOfService == "12-01-2023"
        assert service_data.provideNumber == 123456789
        assert service_data.memberNumber == 987654321
        assert service_data.serviceCode == 900000000
        assert service_data.comments == "Hay Girl"
