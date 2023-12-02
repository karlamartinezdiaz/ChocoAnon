import pytest
from unittest.mock import patch
from manager_controller import ManagerControl
from data import BasicData


@pytest.fixture
def manager_control():
    return ManagerControl()


@pytest.fixture
def provider_object():
    return BasicData("Provider Name", 111111111, "123 Provider Street", "Provider City", "Provider State", 12345)


@pytest.fixture
def member_object():
    return BasicData("Member Name", 222222222, "123 Member Street", "Member City", "Member State", 12345)


@patch('manager_controller.db.addMember')
def test_add_member_success(mock_add_member, manager_control, member_object):
    mock_add_member.return_value = None
    result = manager_control.addMember(member_object)
    assert result == "Member Successfully Added"


@patch('manager_controller.db.addMember')
def test_add_Member_type_error(mock_add_member, manager_control, member_object):
    mock_add_member.side_effect = TypeError("Invalid Member dictionary")
    result = manager_control.addMember(member_object)
    assert isinstance(result, TypeError)
    assert str(result) == "Invalid Member dictionary"


@patch('manager_controller.db.addMember')
def test_add_Member_value_error(mock_add_member, manager_control, member_object):
    mock_add_member.side_effect = ValueError(
        "A Member with that ID already exists in the registry")
    result = manager_control.addMember(member_object)
    assert isinstance(result, ValueError)
    assert str(result) == "A Member with that ID already exists in the registry"


@patch('manager_controller.db.addMember')
@patch('manager_controller.db.deleteMember')
def test_edit_member_success(mock_delete_member, mock_add_member, manager_control, member_object):
    mock_delete_member.return_value = None
    mock_add_member.return_value = None
    member_id = 111111111
    result = manager_control.editMember(member_id, member_object)
    assert result == "Member Information Updated"
    mock_delete_member.assert_called_once_with(member_id)
    mock_add_member.assert_called_once()


@patch('manager_controller.db.addMember')
@patch('manager_controller.db.deleteMember')
def test_edit_member_exception(mock_delete_member, mock_add_member, manager_control, member_object):
    mock_delete_member.side_effect = Exception("Database error")
    member_id = 456789765
    result = manager_control.editMember(member_id, member_object)
    assert isinstance(result, Exception)
    assert str(result) == "Database error"


@patch('manager_controller.db.deleteMember')
def test_remove_provider_success(mock_delete_member, manager_control):
    mock_delete_member.return_value = None
    member_id = 123456789
    result = manager_control.removeMember(member_id)
    assert result == "Member Deleted"


@patch('manager_controller.db.deleteMember')
def test_remove_provider_exception(mock_delete_member, manager_control):
    mock_delete_member.side_effect = Exception("Database error")
    member_id = 123456789
    result = manager_control.removeMember(member_id)
    assert isinstance(result, Exception)
    assert str(result) == "Database error"


@patch('manager_controller.db.addProvider')
def test_add_provider_success(mock_add_provider, manager_control, provider_object):
    mock_add_provider.return_value = None
    result = manager_control.addProvider(provider_object)
    assert result == "Provider Successfully Added"


@patch('manager_controller.db.addProvider')
def test_add_provider_type_error(mock_add_provider, manager_control, provider_object):
    mock_add_provider.side_effect = TypeError("Invalid provider dictionary")
    result = manager_control.addProvider(provider_object)
    assert isinstance(result, TypeError)
    assert str(result) == "Invalid provider dictionary"


@patch('manager_controller.db.addProvider')
def test_add_provider_value_error(mock_add_provider, manager_control, provider_object):
    mock_add_provider.side_effect = ValueError(
        "A provider with that ID already exists in the registry")
    result = manager_control.addProvider(provider_object)
    assert isinstance(result, ValueError)
    assert str(result) == "A provider with that ID already exists in the registry"


@patch('manager_controller.db.deleteProvider')
def test_remove_provider_success(mock_delete_provider, manager_control):
    mock_delete_provider.return_value = None
    provider_id = 123456789
    result = manager_control.removeProvider(provider_id)
    assert result == "Provider Deleted"


@patch('manager_controller.db.deleteProvider')
def test_remove_provider_exception(mock_delete_provider, manager_control):
    mock_delete_provider.side_effect = Exception("Database error")
    provider_id = 123456789
    result = manager_control.removeProvider(provider_id)
    assert isinstance(result, Exception)
    assert str(result) == "Database error"


@patch('manager_controller.db.addProvider')
@patch('manager_controller.db.deleteProvider')
def test_edit_provider_success(mock_delete_provider, mock_add_provider, manager_control, provider_object):
    mock_delete_provider.return_value = None
    mock_add_provider.return_value = None
    provider_id = 123456789
    result = manager_control.editProvider(provider_id, provider_object)
    assert result == "Provider Information Updated"
    mock_delete_provider.assert_called_once_with(provider_id)
    mock_add_provider.assert_called_once()


@patch('manager_controller.db.addProvider')
@patch('manager_controller.db.deleteProvider')
def test_edit_provider_exception(mock_delete_provider, mock_add_provider, manager_control, provider_object):
    mock_delete_provider.side_effect = Exception("Database error")
    provider_id = 123456789
    result = manager_control.editProvider(provider_id, provider_object)
    assert isinstance(result, Exception)
    assert str(result) == "Database error"


@patch('manager_controller.db.getJSONListOfDicts')
def test_get_provider_name_found(mock_get_json_list_of_dicts, manager_control):
    mock_get_json_list_of_dicts.return_value = [
        {
            "name": "Amrit Thapa",
            "Id": 111111111,
            "address": "113 1st Way",
            "city": "Portland",
            "state": "OR",
            "zipcode": 97201,
            "status": "Valid"
        }]
    provider_id = 111111111
    result = manager_control.getProviderName(provider_id)
    assert result == 'Amrit Thapa'


@patch('manager_controller.db.getJSONListOfDicts')
def test_get_provider_name_not_found(mock_get_json_list_of_dicts, manager_control):
    mock_get_json_list_of_dicts.return_value = [
        {
            "name": "Amrit Thapa",
            "Id": 111111111,
            "address": "113 1st Way",
            "city": "Portland",
            "state": "OR",
            "zipcode": 97201,
            "status": "Valid"
        }]
    provider_id = 888888888
    result = manager_control.getProviderName(provider_id)
    assert result is None


@patch('manager_controller.db.getJSONListOfDicts')
def test_get_member_name_found(mock_get_json_list_of_dicts, manager_control):
    mock_get_json_list_of_dicts.return_value = [
        {
            "name": "John Smith",
            "Id": 111333111,
            "address": "123 Main Street",
            "city": "Portland",
            "state": "OR",
            "zipcode": 97201,
            "status": "Valid"
        }]
    member_id = 111333111
    result = manager_control.getMemberName(member_id)
    assert result == 'John Smith'


@patch('manager_controller.db.getJSONListOfDicts')
def test_get_member_name_not_found(mock_get_json_list_of_dicts, manager_control):
    mock_get_json_list_of_dicts.return_value = [
        {
            "name": "John Smith",
            "Id": 111333111,
            "address": "123 Main Street",
            "city": "Portland",
            "state": "OR",
            "zipcode": 97201,
            "status": "Valid"
        }
    ]
    member_id = 987987987
    result = manager_control.getMemberName(member_id)
    assert result is None


def test_get_total_fee_multiple_services(manager_control):
    service_list = [
        {
            "date": "1-1-2023",
            "received": {
                "date": "1-1-2023",
                "time": "08:30:00"
            },
            "memberName": "Member1",
            "memberId": 111333111,
            "serviceCode": 123456,
            "fee": 150
        },
        {
            "date": "1-7-2023",
            "received": {
                "date": "1-7-2023",
                "time": "15:55:48"
            },
            "memberName": "Member2",
            "memberId": 222444222,
            "serviceCode": 123456,
            "fee": 150
        }
    ]
    total_fee = manager_control.getTotalFee(service_list)
    assert total_fee == 300
