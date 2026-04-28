import os
from reservation import TableReservation
from menu import MenuManagement


class OrderSystem:

    def __init__(self, reservation_obj, menu_obj):
        # Use SAME objects from main.py (IMPORTANT)
        self.reservation_obj = reservation_obj
        self.menu_obj = menu_obj
        self.order_file = "data/orders.txt"

    # ---------- GENERATE ORDER ID ----------
    def generate_order_id(self):
        if not os.path.exists(self.order_file):
            return 1

        with open(self.order_file, "r") as file:
            return len(file.readlines()) + 1

    # ---------- VIEW RESERVED TABLES ----------
    def view_reserved_tables(self):
        self.reservation_obj.view_reservations()

    # ---------- TAKE ORDER ----------
    def take_order(self):
        print("\n------ TAKE ORDER ------")

        # Step 1: Show reserved tables
        self.view_reserved_tables()

        if not self.reservation_obj.reservations:
            print("❌ No reserved tables available.")
            return

        # Step 2: Select table
        table = input("Enter Table Number: ")

        # Create valid table list
        reserved_tables = [str(i + 1) for i in range(len(self.reservation_obj.reservations))]

        if table not in reserved_tables:
            print("❌ Invalid table! Please select from reserved tables.")
            return

        # Step 3: Show menu
        print("\n📋 MENU:")
        self.menu_obj.display_menu()

        # Step 4: Take order input
        customer_name = input("Enter Customer Name: ")
        order_id = self.generate_order_id()

        items = []

        while True:
            item = input("Enter Item Name (or 'done'): ").strip()

            if item.lower() == "done":
                break

            try:
                qty = int(input("Enter Quantity: "))
            except ValueError:
                print("❌ Invalid quantity.")
                continue

            items.append((item, qty))

        if not items:
            print("⚠️ No items selected.")
            return

        # Step 5: Save order
        self.save_order(order_id, customer_name, table, items)

    # ---------- SAVE ORDER ----------
    def save_order(self, order_id, name, table, items):
        if not os.path.exists("data"):
            os.makedirs("data")

        with open(self.order_file, "a") as file:
            items_str = ";".join([f"{i}:{q}" for i, q in items])
            file.write(f"{order_id},{name},{table},{items_str}\n")

        print("✅ Order saved successfully!")

    # ---------- VIEW ORDERS ----------
    def view_orders(self):
        print("\n------ ORDER HISTORY ------")

        if not os.path.exists(self.order_file):
            print("No orders found.")
            return

        with open(self.order_file, "r") as file:
            for line in file:
                oid, name, table, items = line.strip().split(",")

                print(f"\nOrder ID: {oid}")
                print(f"Customer: {name}")
                print(f"Table: {table}")

                for i in items.split(";"):
                    item, qty = i.split(":")
                    print(f"  - {item} x {qty}")