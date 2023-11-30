from datetime import datetime


class BasicData:
    def __init__(self, name='', Id=0, address='', city='', state='', zipcode=0):
        self.name = name
        self.Id = Id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode

    def getName(self):
        name = input("Please enter your name(less than 25 characters): ")
        while True:
            if len(name) > 25:
                print("Name more than 25 characters. Try Again")
            else:
                return name

    def getCity(self):
        city = input("Please enter your city(less than 14 characters): ")
        while True:
            if len(city) > 14:
                print("city more than 14 characters. Try Again")
            else:
                return city

    def getState(self):
        state = input("Please enter state initials (2 characters): ")
        while True:
            if len(state) > 2:
                print("More than 2 chars entered. Try Again")
            else:
                return state

    def getAddress(self):
        address = input("Please enter your address(less than 25 characters): ")
        while True:
            if len(address) > 25:
                print("address more than 25 characters. Try Again")
            else:
                return address

    def getId(self):
        while True:
            Id = input("Enter your 9 digit id: ")
            if not Id.isdigit():
                print("The id should only contain numbers")
            elif len(Id) != 9:
                print("The Id must have exactly 9 numbers")
            else:
                return int(Id)

    def getZipcode(self):
        while True:
            Zipcode = input("Enter your Zipcode: ")
            if not Zipcode.isdigit():
                print("The Zipcode should only contain numbers")
            elif len(Zipcode) != 5:
                print("The Zipcode must have exactly 5 numbers")
            else:
                return int(Zipcode)

    def createBasicData(self):
        name = self.getName()
        Id = self.getId()
        address = self.getAddress()
        city = self.getCity()
        state = self.getState()
        zipcode = self.getZipcode()
        return BasicData(name, Id, address, city, state, zipcode)


class ServiceData:
    def __init__(self, time='', dateOfService='', providerNumber=0, memberNumber=0, serviceCode=0, comments=''):
        self.time = time
        self.dateOfService = dateOfService
        self.providerNumber = providerNumber
        self.memberNumber = memberNumber
        self.serviceCode = serviceCode
        self.comments = comments

    def getDateOfService(self):
        date = input("Please type in your date of service(MM-DD-YYYY): ")
        dateOfService = datetime.strptime(date, "%m-%d-%Y")
        return dateOfService.strftime('%d-%m-%Y')

    def getDateAndTime(self):
        dateNTime = datetime.now()
        return datetime.strftime(dateNTime, '%m-%d-%Y %H:%M:S')

    def getProviderNumber(self):
        while True:
            providerNumber = (input("Enter the provider number: "))
            if not providerNumber.isdigit():
                print("The provider Number should only contain numbers")
            elif len(providerNumber) != 9:
                print("The provider number must have exaclty 9 numbers")
            else:
                return int(providerNumber)

    def getMemberNumber(self):
        while True:
            memberNumber = (input("Enter the member number: "))
            if not memberNumber.isdigit():
                print("The member Number should only contain numbers")
            elif len(memberNumber) != 9:
                print("The member number must have exaclty 9 numbers")
            else:
                return int(memberNumber)

    def getServiceCode(self):
        while True:
            serviceCode = (input("Enter the service code: "))
            if not serviceCode.isdigit():
                print("The service code should only contain numbers")
            elif len(serviceCode) != 6:
                print("The service code must have exaclty 9 numbers")
            else:
                return int(serviceCode)

    def getComment(self):
        while True:
            comment = input("Enter your comment (less than 100 characters): ")
            if len(comment) > 100:
                print("Too many characters. Must be below 100 ")
            else:
                return comment

    def createServiceData(self):
        time = self.getDateAndTime()
        dateOfService = self.getDateOfService()
        providerNumber = self.getProviderNumber()
        memberNumber = self.getMemberNumber()
        serviceCode = self.getServiceCode()
        comments = self.getComment()
        return ServiceData(time, dateOfService, providerNumber, memberNumber, serviceCode, comments)
