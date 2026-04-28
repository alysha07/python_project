class TableReservation:

    def __init__(self):
        self.reservations = []

    def take_reservation(self):
        name = input("Enter customer name: ")
        date = input("Enter date (DD-MM-YYYY): ")
        time = input("Enter time (HH:MM): ")
        people = input("Enter number of people: ")

        return {
            "name": name,
            "date": date,
            "time": time,
            "people": people
        }

    def confirm_reservation(self, temp):
        print("\nPlease confirm your details:")
        print(f"Name: {temp['name']}")
        print(f"Date: {temp['date']}")
        print(f"Time: {temp['time']}")
        print(f"People: {temp['people']}")

        choice = input("Confirm? (yes/no): ").lower()

        if choice == "yes":
            self.reservations.append(temp)
            print("Reservation confirmed!")
        else:
            print("Cancelled")

    def view_reservations(self):
        if not self.reservations:
            print("No reservations")
            return

        print("\n--- Reservations ---")
        for i, r in enumerate(self.reservations, 1):
            print(i, r)