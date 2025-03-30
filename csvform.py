import csv

def generate_student_id(filename='students.csv'):
    """Generate a unique student ID by checking the last one in the CSV."""
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            last_id = rows[-1][0] if len(rows) > 1 else 'S1000'  # Handle case where file is empty
            student_id_number = int(last_id[1:]) + 1
            return f"S{student_id_number:04d}"
    except FileNotFoundError:
        return 'S1001'  # Default ID for first record

def save_to_csv(data, filename='students.csv'):
    """Save the form data into a CSV file."""
    headers = ['Student ID', 'Name', 'Parents Name', 'Phone Number', 'Email Address']
    
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Check if the file is empty and write headers if necessary
            file_empty = file.tell() == 0
            if file_empty:
                writer.writerow(headers)
            
            # Write the submitted data to the CSV
            writer.writerow(data)
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data: {e}")
