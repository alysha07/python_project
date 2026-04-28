# Restaurant Menu System
from menu import MenuManagement
from reservation import TableReservation

menu = MenuManagement()
reservation_obj = TableReservation()

def main():
    while True:
        print("\n====== RESTAURANT MENU SYSTEM ======")
        print("1. Admin")
        print("2. Customer")
        print("3. Waiter")
        print("4. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            while True:
                print("\n------ ADMIN MENU ------")
                print("1. Add Item")
                print("2. Show Menu")
                print("3. Search Item")
                print("4. Update Item")
                print("5. Delete Item")
                print("6. Exit")

                admin_choice = int(input("Enter choice: "))

                if admin_choice == 1:
                    menu.add_item()

                elif admin_choice == 2:
                    menu.show_menu()

                elif admin_choice == 3:
                    menu.search_item()

                elif admin_choice==4:
                    menu.update_item()    

                elif admin_choice == 5:
                    menu.delete_item()

                elif admin_choice == 6:
                    break

                else:
                    print("Invalid choice!")

        elif choice == 2:
            while True:
                print("\n------ CUSTOMER MENU ------")
                print("1. Display Menu")
                print("2. Reserve table")
                print("3. Exit")

                customer_choice = int(input("Enter choice: "))
                if customer_choice == 1:
                    menu.display_menu()
                elif customer_choice == 2:
                    
                    data = reservation_obj.take_reservation()
                    reservation_obj.confirm_reservation(data)

                elif customer_choice == 3:
                    break
                else:
                    print("Invalid choice!")

        elif choice == 3:
            while True:
                print("\n------ WAITER MENU ------")
                print("1. View Reservation")
                print("2. Take Order")
                print("3. Exit")
                waiter_choice = int(input("Enter choice: "))
                if waiter_choice == 1:
                    reservation_obj.view_reservations()
                elif waiter_choice == 2:
                 take_order()

                elif waiter_choice == 3:
                    break
                else:
                    print("Invalid choice!")

        elif choice == 4:
            print("Exiting program...")
            break

        else:
            print("Invalid choice!")
# Run program
main()