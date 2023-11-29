from database import *
import pytest
import os


path = "test1.json"
data = {
	'name': "simon",
	'status': "amazing",
	'age': 99
}
data2 = {
	'name': "charles",
	'status': "sub-par",
	'age': 123 
}

data_list = [data, data2]


#createJSONFile() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_create_new_json_file():
	assert not os.path.isfile(path)
	
	createJSONFile(path, data)
	assert os.path.isfile(path)
	
	with open(path, "r") as file:
		jsonData = json.load(file)	
		file.close()

	assert jsonData['name'] == "simon"
	assert jsonData['status'] == "amazing"
	assert jsonData['age'] == 99

	os.remove(path)


def test_overwrite_json_file():
	createJSONFile(path, data)

	createJSONFile(path, data2)

	with open(path, "r") as file:
		jsonData = json.load(file)
		file.close()
	
	assert jsonData['name'] == "charles"
	assert jsonData['status'] == "sub-par"
	assert jsonData['age'] == 123

	os.remove(path)



@pytest.mark.xfail(raises = TypeError)
def test_create_json_file_bad_dict():
	list = [1, 2, 3]
	createJSONFile(path, list)



@pytest.mark.xfail(raises = TypeError)
def test_create_json_file_bad_path():
	list = [1, 2, 3]
	createJSONFile(list, data)


#createJSONListFile() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_create_new_jsons_list_file():
	assert not os.path.isfile(path)

	createJSONListFile(path, data_list)
	assert os.path.isfile(path)

	with open(path, "r") as file:
		jsonData = json.load(file)
		file.close()
	assert jsonData[0] == data
	assert jsonData[1] == data2
	
	os.remove(path)


def test_overwrite_json_list_file():
	createJSONListFile(path, data_list)

	new_list = [data2, data]
	createJSONListFile(path, new_list)

	with open(path, "r") as file:
		jsonData = json.load(file)
		file.close()
	
	assert jsonData[0] == data2
	assert jsonData[1] == data

	os.remove(path)

@pytest.mark.xfail(raises = TypeError)
def test_json_list_bad_list():
	not_a_list = 123
	createJSONListFile(path, not_a_list)


@pytest.mark.xfail(raises = TypeError)
def test_json_list_bad_path():
	bad_path = [1, 2, 3]
	createJSONListFile(bad_path, data_list)


#getJSONDict() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_get_json_dict():
	createJSONFile(path, data)

	dictionary = getJSONDict(path)

	assert dictionary == data

	os.remove(path)

@pytest.mark.xfail(raises = ValueError)
def test_get_json_dict_not_json():
	new_path = "database.py"
	dictionary = getJSONDict(new_path)


@pytest.mark.xfail(raises = IOError)
def test_get_json_dict_no_file():
	bad_path = "this_file_does_not_exist.json"
	dictionary = getJSONDict(bad_path)


@pytest.mark.xfail(raises = ValueError)
def test_get_json_dict_not_dict():
	dictionary = getJSONDict("database/provider_directory.json")



#getJSONListOfDicts() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_get_json_list():
	createJSONListFile(path, data_list)
	list = getJSONListOfDicts(path)

	assert list == data_list

	os.remove(path)


@pytest.mark.xfail(raises = ValueError)
def test_get_json_list_no_json():
	bad_path = "database.py"
	list = getJSONListOfDicts(bad_path)


@pytest.mark.xfail(raises = IOError)
def test_get_json_list_no_file():
	bad_path = "this_file_does_not_exist.json"
	list = getJSONListOfDicts(bad_path)


@pytest.mark.xfail(raises = ValueError)
def test_get_json_list_not_list():
	createJSONFile(path, data)
	try:
		list = getJSONListOfDicts(path)

	except ValueError:
		os.remove(path)
		raise


#checkProviderID() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_provider_id_valid():
	assert checkProviderID(111111111)

def test_provider_id_invalid():
	assert not checkProviderID(999999999)



#checkMemberID() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_member_id_valid():
	assert checkMemberID(111333111) == "Valid"

def test_member_id_invalid():
	assert checkMemberID(999999999) == "Invalid"


#checkServiceCode() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_service_code_valid():
	assert checkServiceCode(123456)


def test_service_code_invalid():
	assert not checkServiceCode(333333)



test_member = {
	"name": "Member9",
    "Id": 123456789,
    "address": "224 22nd St",
    "city": "Two Town",
    "state": "OR",
    "zipcode": 22222,
    "status": "Valid"	
}

test_provider = {
	"name": "prov9",
    "Id": 987654321,
    "address": "lalkdjf",
    "city": "slfjk",
    "state": "kj",
    "zipcode": 98987	
}
#addMember() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_add_valid_member():
	addMember(test_member)
	with open("database/member_registry.json", "r") as file:
		jsonData = json.load(file)
		file.close()

	match = False
	for member in jsonData:
		if member == test_member:
			match = True

	assert match
	deleteMember(test_member['Id'])


@pytest.mark.xfail(raises = TypeError)
def test_add_member_not_dict():
	addMember("hello!")


@pytest.mark.xfail(raises = ValueError)
def test_add_member_duplicate():
	addMember(test_member)
	try:
		addMember(test_member)
	except ValueError:
		deleteMember(test_member['Id'])
		raise

#addProvider() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_add_valid_provider():
	addProvider(test_provider)
	with open("database/provider_registry.json", "r") as file:
		jsonData = json.load(file)
		file.close()

	match = False
	for provider in jsonData:
		if provider == test_provider:
			match = True

	assert match
	deleteProvider(test_provider['Id'])


@pytest.mark.xfail(raises = TypeError)
def test_add_provider_not_dict():
	addProvider("hello!")


@pytest.mark.xfail(raises = ValueError)
def test_add_provider_duplicate():
	addProvider(test_provider)
	try:
		addProvider(test_provider)
	except ValueError:
		deleteProvider(test_provider['Id'])
		raise


#deleteMember() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_delete_valid_member():
	addMember(test_member)
	deleteMember(test_member['Id'])

	with open("database/member_registry.json", "r") as file:
		jsonData = json.load(file)
		file.close()
	
	match = False
	for member in jsonData:
		if member == test_member:
			match = True

	assert not match


@pytest.mark.xfail(raises = ValueError)
def test_delete_invalid_member():
	deleteMember(test_member['Id'])


@pytest.mark.xfail(raises = TypeError)
def test_delete_member_not_int():
	deleteMember("hello")


#deleteProvider() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_delete_valid_provider():
	addProvider(test_provider)
	deleteProvider(test_provider['Id'])

	with open("database/provider_registry.json", "r") as file:
		jsonData = json.load(file)
		file.close()
	
	match = False
	for provider in jsonData:
		if provider == test_provider:
			match = True

	assert not match


@pytest.mark.xfail(raises = ValueError)
def test_delete_invalid_provider():
	deleteProvider(test_provider['Id'])


@pytest.mark.xfail(raises = TypeError)
def test_delete_provider_not_int():
	deleteProvider("hello")


