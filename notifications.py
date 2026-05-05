import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print(f"❌ Could not send email: {e}")


def reservation_confirmation_email(customer_name, customer_email, date, time, guests):
    body = f"""
    <h2>🪑 Reservation Confirmed!</h2>
    <p>Dear <b>{customer_name}</b>,</p>
    <p>Your table has been successfully reserved!</p>
    <h3>Booking Details:</h3>
    <ul>
        <li>Date: <b>{date}</b></li>
        <li>Time: <b>{time}</b></li>
        <li>Guests: <b>{guests}</b></li>
    </ul>
    <p>We look forward to seeing you! 😊</p>
    <p><i>— Restaurant Team</i></p>
    """
    send_email(customer_email, "Table Reservation Confirmed! 🪑", body)


def review_request_email(customer_name, customer_email, order_id):
    body = f"""
    <h2>Thank you for dining with us! 🍽</h2>
    <p>Dear <b>{customer_name}</b>,</p>
    <p>We hope you enjoyed your meal (Order <b>#{order_id}</b>)!</p>
    <p>We'd love to hear your feedback. Please reply to this email with your rating:</p>
    <h3>Rate us:</h3>
    <p>
        ⭐ Poor &nbsp;&nbsp;
        ⭐⭐ Fair &nbsp;&nbsp;
        ⭐⭐⭐ Good &nbsp;&nbsp;
        ⭐⭐⭐⭐ Great &nbsp;&nbsp;
        ⭐⭐⭐⭐⭐ Excellent
    </p>
    <p>We look forward to serving you again! 😊</p>
    <p><i>— Restaurant Team</i></p>
    """
    send_email(customer_email, "How was your experience? ⭐ Leave us a Review!", body)
