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


@pytest.fixture
def test_manager():
    return ManagerControl()

# def test_manager_control():
    # manager_instance = ManagerControl()
    # assert manager_instance is not None


def test_make_dict(test_manager: ManagerControl):
    test_object = TestDataObject(
        "Karla Martinez", 123456789, "246 Sally St", "Portland", "OR", "97123")

    expected_result = {
        'name': 'Karla Martinez',
        'Id': 123456789,
        'address': '246 Sally St',
        'city': 'Portland',
        'state': 'OR',
        'zipcode': '97123'
    }

    result_dict = test_manager.makeDict(test_object)
    assert result_dict == expected_result

#####################################


def test_add_provider(test_manager: ManagerControl):
    test_provider_info = TestDataObject(
        "Provider", 1234, "246 Sally St", "Portland", "OR", "97123")

    result_provider = test_manager.addProvider(test_provider_info)

    test_provider_dict = test_manager.makeDict(result_provider)

    assert test_manager.addProvider(
        test_provider_dict) == "Provider Successfully Added"
