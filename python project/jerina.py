import sqlite3
from datetime import datetime

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
        return f"UPI | ID: {upi_id} | Paid: ₹{amount}"


class CardPayment(Payment):
    def pay(self, amount):
        card_no = input("Enter last 4 digits of card: ")
        return f"Card | XXXX-{card_no} | Paid: ₹{amount}"


# ------------------ DATABASE INIT ------------------

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



#----------------------- overall summary for admin to view ------------------------

def show_summary(today_only=False):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    if today_only:
        today = datetime.now().strftime("%d-%m-%Y")
        cursor.execute("""
        SELECT COUNT(*), SUM(grand_total), SUM(gst), SUM(discount)
        FROM orders
        WHERE date LIKE ?
        """, (f"{today}%",))
    else:
        cursor.execute("""
        SELECT COUNT(*), SUM(grand_total), SUM(gst), SUM(discount)
        FROM orders
        """)

    result = cursor.fetchone()
    conn.close()

    total_orders = result[0] or 0
    total_revenue = result[1] or 0
    total_gst = result[2] or 0
    total_discount = result[3] or 0

    print("\n" + "="*40)
    print("📊 SALES SUMMARY")
    print("="*40)

    if today_only:
        print("📅 Today’s Report\n")

    print(f"Total Orders   : {total_orders}")
    print(f"Total Revenue  : ₹{total_revenue:.2f}")
    print(f"Total GST      : ₹{total_gst:.2f}")
    print(f"Total Discount : ₹{total_discount:.2f}")

    print("="*40 + "\n")

# ------------------ BILL SUMMARY  ------------------

def show_bill_summary(order, menu):
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

    # PRINT SUMMARY
    print("\n" + "="*40)
    print("🧾 BILL SUMMARY (Before Payment)")
    print("="*40)

    for item, qty, price, total in bill_lines:
        print(f"{item:<15}{qty:<5}{price:<8}{total:<10}")

    print("-"*40)
    print(f"Subtotal: ₹{subtotal:.2f}")
    print(f"Discount: -₹{discount:.2f}")
    print(f"GST: ₹{gst:.2f}")
    print(f"Grand Total: ₹{grand_total}")
    print("="*40)

    return grand_total, subtotal, discount, gst, bill_lines


# ------------------ BILLING SYSTEM ------------------

def generate_bill(order, menu):
    init_db()

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    #  Show summary BEFORE payment
    grand_total, subtotal, discount, gst, bill_lines = show_bill_summary(order, menu)

    #  Confirmation
    confirm = input("Proceed to payment? (y/n): ")
    if confirm.lower() != "y":
        print("❌ Order cancelled.\n")
        return

    # -------- PAYMENT --------
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
            print("Invalid choice. Try again.")
            continue

        payment_info = payment.pay(grand_total)

        if payment_info is not None:
            break
        else:
            print("Retry payment...\n")

    # Prepare item string for DB
    items_str = ""
    for item, qty in order.items():
        items_str += f"{item}({qty}) | "

    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    # -------- SAVE TO DATABASE --------
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
# auto-generated Order ID
    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    # -------- FINAL BILL PRINT --------
    print("\n" + "="*40)
    print("        🍽️ RESTAURANT BILL")
    print("="*40)
    print(f"Order ID : {order_id}")
    print(f"Date     : {date}")
    print("-"*40)

    for item, qty, price, total in bill_lines:
        print(f"{item:<15}{qty:<5}{price:<8}{total:<10}")

    print("-"*40)
    print(f"Subtotal: ₹{subtotal:.2f}")
    print(f"Discount: -₹{discount:.2f}")
    print(f"GST: ₹{gst:.2f}")
    print(f"Grand Total: ₹{grand_total}")
    print("-"*40)
    print(f"Payment: {payment_info}")
    print("="*40)
    print("🙏 Thank you! Visit again!\n")

    return grand_total


# ------------------ TEST RUN ------------------

if __name__ == "__main__":

    menu = {
        "Burger": 120,
        "Fries": 80,
        "Pizza": 250,
        "Coke": 50
    }

    order = {
        "Burger": 2,
        "Fries": 1
    }

    generate_bill(order, menu)