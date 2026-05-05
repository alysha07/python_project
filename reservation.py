class TableReservation:

    def __init__(self):
        self.reservations = []

    def take_reservation(self):
        name = input("Enter customer name: ")
        date = input("Enter date (DD-MM-YYYY): ")
        time = input("Enter time (HH:MM): ")
        guest = input("Enter number of guest: ")

        return {
            "name": name,
            "date": date,
            "time": time,
            "guest": guest
        }

    def confirm_reservation(self, temp):
        print("\nPlease confirm your details:")
        print(f"Name: {temp['name']}")
        print(f"Date: {temp['date']}")
        print(f"Time: {temp['time']}")
        print(f"Guests: {temp['guest']}")

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
          print(f"\nReservation {i}")
          print(f"Name        : {r['name']}")
          print(f"Date        : {r['date']}")
          print(f"Time        : {r['time']}")
          print(f"Guests      : {r['guest']}")
          print("-" * 25)