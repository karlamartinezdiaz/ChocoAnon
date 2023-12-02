import pytest
from manager_controller import *
from database import *
from data import *


def testMakeDict():
    manager = ManagerControl()
    data = BasicData("Amrit Thapa", 765987098, "3011 Main St",
                     "Portland", "Oregon", 54321)
    expected_dict = {
        "name": "Amrit Thapa",
        "Id": 765987098,
        "address": "3011 Main St",
        "city": "Portland",
        "state": "Oregon",
        "zipcode": 54321
    }
    assert manager.makeDict(data) == expected_dict


def testAddProvider():
    pass
