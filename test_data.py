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
