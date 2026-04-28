import sqlite3
from datetime import datetime
from getpass import getpass

# ------------------ PAYMENT ------------------

class Payment:
    def pay(self, amount):
        return "Unknown Payment"


class CashPayment(Payment):
    def pay(self, amount):
        given = float(input("Enter cash given: ₹"))
        if given < amount:
            print("❌ Not enough cash!")
            return None
        change = given - amount
        return f"Cash | Paid: ₹{given} | Change: ₹{change}"


class UPIPayment(Payment):
    def pay(self, amount):
        upi_id = input("Enter UPI ID: ")
        pin = getpass("Enter UPI PIN (hidden): ")

        if len(pin) < 4:
            print("❌ Invalid PIN")
            return None

        return f"UPI | ID: {upi_id} | Paid: ₹{amount}"


class CardPayment(Payment):
    def pay(self, amount):
        card_no = input("Enter last 4 digits of card: ")
        pin = getpass("Enter Card PIN (hidden): ")

        if len(pin) < 4:
            print("❌ Invalid PIN")
            return None

        return f"Card | XXXX-{card_no} | Paid: ₹{amount}"


# ------------------ DATABASE ------------------

def init_db():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        items TEXT,
        subtotal REAL,
        discount REAL,
        gst REAL,
        grand_total REAL,
        payment TEXT
    )
    """)

    conn.commit()
    conn.close()


# ------------------ BILL CALCULATION ------------------

def calculate_bill(order, menu):
    subtotal = 0
    bill_lines = []

    for item, qty in order.items():
        price = menu[item]
        total = price * qty
        subtotal += total
        bill_lines.append((item, qty, price, total))

    # Discount
    discount = 0
    if subtotal > 500:
        discount = subtotal * 0.10

    # GST
    taxable = subtotal - discount
    gst = taxable * 0.05
    grand_total = round(taxable + gst)

    return subtotal, discount, gst, grand_total, bill_lines


# ------------------ BILL SUMMARY ------------------

def show_bill(order, menu):
    subtotal, discount, gst, grand_total, bill_lines = calculate_bill(order, menu)

    print("\n" + "="*50)
    print("🍽️ RESTAURANT BILL".center(50))
    print("="*50)

    print("Table No: 1")
    print("-"*50)
    print(f"{'Item':<15}{'Qty':<8}{'Price':<10}{'Total'}")
    print("-"*50)

    for item, qty, price, total in bill_lines:
        print(f"{item:<15}{qty:<8}{price:<10}{total}")

    print("-"*50)
    print(f"{'Subtotal:':<25}₹{subtotal:.2f}")
    print(f"{'Discount:':<25}-₹{discount:.2f}")
    print(f"{'GST (5%):':<25}₹{gst:.2f}")
    print("-"*50)
    print(f"{'TOTAL:':<25}₹{grand_total:.2f}")
    print("="*50)

    return subtotal, discount, gst, grand_total, bill_lines


# ------------------ GENERATE BILL ------------------

def generate_bill(order, menu):
    init_db()
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    # Step 1: Show bill first
    subtotal, discount, gst, grand_total, bill_lines = show_bill(order, menu)

    # Step 2: confirm
    confirm = input("\nProceed to payment? (y/n): ")
    if confirm.lower() != "y":
        print("❌ Order Cancelled\n")
        return

    # Step 3: payment selection
    print("\nSelect Payment Method:")
    print("1. Cash\n2. UPI\n3. Card")

    while True:
        choice = input("Enter choice: ")

        if choice == "1":
            payment = CashPayment()
        elif choice == "2":
            payment = UPIPayment()
        elif choice == "3":
            payment = CardPayment()
        else:
            print("Invalid choice")
            continue

        payment_info = payment.pay(grand_total)

        if payment_info is not None:
            break
        else:
            print("Retry payment...\n")

    # Step 4: save items string
    items_str = ""
    for item, qty in order.items():
        items_str += f"{item}({qty}) | "

    # Step 5: date
    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    # Step 6: save to DB
    cursor.execute("""
    INSERT INTO orders
    (date, items, subtotal, discount, gst, grand_total, payment)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        date,
        items_str,
        subtotal,
        discount,
        gst,
        grand_total,
        payment_info
    ))

    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # ---------------- FINAL RECEIPT ----------------

    print("\n" + "="*50)
    print("🍽️ RESTAURANT BILL".center(50))
    print("="*50)

    print(f"Order ID : {order_id}")
    print(f"Date     : {date}")
    print("-"*50)
    print(f"{'Item':<15}{'Qty':<8}{'Price':<10}{'Total'}")
    print("-"*50)

    for item, qty, price, total in bill_lines:
        print(f"{item:<15}{qty:<8}{price:<10}{total}")

    print("-"*50)
    print(f"{'Subtotal:':<25}₹{subtotal:.2f}")
    print(f"{'Discount:':<25}-₹{discount:.2f}")
    print(f"{'GST (5%):':<25}₹{gst:.2f}")
    print("-"*50)
    print(f"{'TOTAL:':<25}₹{grand_total:.2f}")
    print("-"*50)
    print(f"Payment: {payment_info}")
    print("="*50)
    print("🙏 Thank you! Visit again!\n")


# ------------------ TEST RUN ------------------

if __name__ == "__main__":

    menu = {
        "Biryani": 200,
        "Burger": 120,
        "Fries": 80,
        "Coke": 50
    }

    order = {
        "Biryani": 1
    }

    generate_bill(order, menu)