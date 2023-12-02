from manager_controller import ManagerControl
import pytest


class TestDataObject:
    def __init__(self, name, Id, address, city, state, zipcode):
        self.name = name
        self.Id = Id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode


def manager_instance():
    return ManagerControl()


def test_manager_control(manager_instance):
    with pytest.raises(ValueError, match="Invalid member ID"):
        manager_instance.removeMember(22244422)


def test_MakeDict(manager_instance):
    test_object = TestDataObject(
        name="Yo mama", Id=123456789, address="246 Sally St", city="Portland", state="OR", zipcode=97123)
    result_dict = manager_instance.makeDict(test_object)

    expected_result = {
        'name': 'Yo mama',
        'Id': 123456789,
        'address': '246 Sally St',
        'city': 'Portland',
        'state': 'OR',
        'zipcode': '97123'
    }

    assert result_dict == expected_result
