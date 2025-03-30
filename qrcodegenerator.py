import os
import qrcode
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from flask import Flask, request, redirect, url_for, render_template
import csv
import qrcode
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

def generate_qr_code(student_id):
    """Generate QR code with student ID and return image bytes."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    payment_url = f"https://payment-portal.com/pay?student_id={student_id}"
    qr.add_data(payment_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    return img_byte_array

def send_payment_email(email, student_id):
    """Send payment QR code to the student's email."""
    qr_code_image = generate_qr_code(student_id)

    msg = MIMEMultipart()
    msg["From"] = "minpyaemusic@gmail.com"
    msg["To"] = email
    msg["Subject"] = "Payment QR Code"

    body = f"Dear Student,\n\nPlease scan the attached QR code to proceed with your payment.\n\nBest regards,\nYour Institution"
    msg.attach(MIMEText(body, "plain"))

    qr_attachment = MIMEImage(qr_code_image.getvalue(), name=f"payment_qr_{student_id}.png")
    msg.attach(qr_attachment)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("minpyaemusic@gmail.com", "tdkq lptj dqhj rbgp")
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


'''
def generate_qr_codes_from_csv(csv_file):
    """Generate QR codes for all student IDs from a CSV file."""
    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)
        # Assuming the student IDs are in the first column of the CSV
        next(csv_reader)  # Skip the header if there's one
        
        for row in csv_reader:
            student_id = row[0]  # Get student ID from the first column
            generate_qr_code(student_id)

# Example: Generate and view QR code for a student
csv_file = 'students.csv'  # The path to your CSV file
generate_qr_codes_from_csv(csv_file)
'''