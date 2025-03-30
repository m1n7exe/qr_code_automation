from flask import Flask, request, render_template, redirect, url_for
from csvform import generate_student_id, save_to_csv
from qrcodegenerator import generate_qr_code, send_payment_email
import csv
# Initialize the Flask app
app = Flask(__name__)
CSV_FILE = 'students.csv'
# Route for the registration form
@app.route('/')
def home():
    return render_template('form.html')  # This is the form page where users enter their information

# Route to handle form submission
@app.route('/submit_student', methods=['POST'])
def handle_form_submission():
    # Get form data from the POST request
    student_name = request.form.get('student_name')
    parents_name = request.form.get('parents_name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    
    # Create a list with the form data
    student_data = [generate_student_id(), student_name, parents_name, phone_number, email]
    
    # Save the form data to the CSV file
    save_to_csv(student_data)
    
    # Redirect to the payment page
    return redirect(url_for('payment_page'))  # Redirect to '/payment'

def get_last_student():
    """Read the last student's email and ID from the CSV file."""
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if len(rows) < 2:  # If only header exists or empty
            return None, None
        last_row = rows[-1]
        return last_row[4], last_row[0]  # Assuming Email is in column 0, ID in column 












@app.route('/send_email', methods=['POST'])
def send_payment_email_route():
    email, student_id = get_last_student()

    if not email or not student_id:
        return "Error: No student data found", 400

    send_payment_email(email, student_id)
    
    return redirect(url_for('payment_success'))

@app.route('/payment_success')
def payment_success():
    return render_template('payment_confirmation.html')

# Route for the payment page
@app.route('/payment')
def payment_page():
    return render_template('payment.html')  # Show the payment page where the user clicks to make a payment

if __name__ == '__main__':
    app.run(debug=True)