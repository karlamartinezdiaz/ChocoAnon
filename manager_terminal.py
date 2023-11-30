
import manager_controller as mc
import data

'''Displays the user options'''


def main_menu():
    print("1. End of Week")
    print("2. Generate ETF Report")
    print("3. Generate Member Reports")
    print("4. Generate Provider Reports")
    print("5. Add Members")
    print("6. Update Member")
    print("7. Remove Member")
    print("8. Add Provider")
    print("9. Update Provider")
    print("10. Remove Provider")
    print("11. Turn Off Terminal")


'''Calls the following three functions.'''


def endOfWeek():
    etfReport()
    memberReport()
    providerReport()


'''Placeholder for manager.py function'''


def etfReport():
    pass


'''Takes in a member id. Calls manager.py function'''


def memberReport():
    print(mc.ManagerControl().viewMemberReport(data.BasicData().getId()))
    # Something should be returned here. At the very least a T/F.


'''Takes in a provider id. Calls manager.py function'''


def providerReport():
    print(mc.ManagerControl().viewProviderReport(data.BasicData().getId()))
    # Something should be returned here. At the very least a T/F.


def addMember():
    print(mc.ManagerControl().addMember(data.BasicData().createBasicData()))
    # Something should be returned here. At the very least a T/F.


def updateMember():
    member = data.BasicData().createBasicData()
    print(mc.ManagerControl().editMember(member.Id, member))
    # Something should be returned here. At the very least a T/F.


def removeMember():
    print(mc.ManagerControl().removeMember(data.BasicData().getId()))
    # Something should be returned here. At the very least a T/F.


def addProvider():
    print(mc.ManagerControl().addProvider(data.BasicData().createBasicData()))
    # Something should be returned here. At the very least a T/F.


def updateProvider():
    provider = data.BasicData().createBasicData()
    print(mc.ManagerControl().editProvider(provider.Id, provider))
    # Something should be returned here. At the very least a T/F.


def removeProvider():
    print(mc.ManagerControl().removeProvider(data.BasicData().getId()))
    # Something should be returned here. At the very least a T/F.


if __name__ == '__main__':
    choice = 1
    while choice != 11:
        try:
            main_menu()
            choice = int(input("Please enter choice: "))

            if choice == 1:
                endOfWeek()
            elif choice == 2:
                etfReport()
            elif choice == 3:
                memberReport()
            elif choice == 4:
                providerReport()
            elif choice == 5:
                addMember()
            elif choice == 6:
                updateMember()
            elif choice == 7:
                removeMember()
            elif choice == 8:
                addProvider()
            elif choice == 9:
                updateProvider()
            elif choice == 10:
                removeMember()
            elif choice == 11:
                pass
            else:
                print("Invalid Choice.")

        # Intended to catch letters/characters.
        except ValueError:
            print("Invalid Choice.")

    print("Shutting off terminal.")
