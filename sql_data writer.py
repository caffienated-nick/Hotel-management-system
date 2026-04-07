import random
import datetime
rooms =[
        "A1", "B1", "C1", "D1", "E1",
        "A2", "B2", "C2", "D2", "E2",
        "A3", "B3", "C3", "D3", "E3",
        "A4", "B4", "C4", "D4", "E4",
        "A5", "B5", "C5", "D5", "E5"
    ]     
# Generate mock data for the tables
def generate_room_assignments_data(num_records=100):
    records = []
    for i in range(1, num_records + 1):
        records.append(f"""
        INSERT INTO room_assignments (
            id, room_name, name, address, date_of_checkin, number_of_people, 
            email, phone_no, extra_services, accomodation_services, events, 
            wellness, pets, private_dining, occasion, adhaar_numbers
        ) VALUES (
            {i}, 
            '{random.choice(rooms)}',
            'Name_{i}', 
            'Address_{i}', 
            '{datetime.date(2024, 1, 1) + datetime.timedelta(days=random.randint(0, 365))}', 
            {random.randint(1, 4)}, 
            'email{i}@example.com', 
            '{random.randint(7000000000, 9999999999)}',
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])},
            '{random.randint(100000000000, 999999999999)}'
        );
        """)
    return records

def generate_food_records_data(num_records=100):
    records = []
    for i in range(1, num_records + 1):
        records.append(f"""
        INSERT INTO Food_records (
            id, Total_bill
        ) VALUES (
            {i}, 
            {random.uniform(50, 500):.2f}
        );
        """)
    return records

def generate_invoice_table_data(num_records=100):
    records = []
    for i in range(1, num_records + 1):
        records.append(f"""
        INSERT INTO invoice_table (
            id, checkout_date, days_stayed, final_bill
        ) VALUES (
            {i}, 
            '{datetime.date(2024, 1, 1) + datetime.timedelta(days=random.randint(0, 365))}', 
            {random.randint(1, 30)}, 
            {random.uniform(200, 5000):.2f}
        );
        """)
    return records

def generate_hotel_records_data(num_records=100):
    records = []
    for i in range(1, num_records + 1):
        records.append(f"""
        INSERT INTO hotel_records (
            id, room_name, name, address, date_of_checkin, number_of_people, email, phone_no, 
            extra_services, accomodation_services, events, wellness, pets, private_dining, occasion, 
            adhaar_numbers, checkout_date, days_stayed, final_bill
        ) VALUES (
            {i}, 
            '{random.choice(rooms)}',
            'Name_{i}', 
            'Address_{i}', 
            '{datetime.date(2024, 1, 1) + datetime.timedelta(days=random.randint(0, 365))}', 
            {random.randint(1, 4)}, 
            'email{i}@example.com', 
            '{random.randint(7000000000, 9999999999)}',
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            {random.choice([True, False])}, 
            'Adhaar_{random.randint(100000000000, 999999999999)}',
            '{datetime.date(2024, 1, 1) + datetime.timedelta(days=random.randint(0, 365))}', 
            {random.randint(1, 30)}, 
            {random.uniform(200, 5000):.2f}
        );
        """)
    return records

# Write to files
def write_sql_file(filename, records):
    with open(f"D:\\codes\\Hotel management system v2\\{filename}", "w") as file:
        file.writelines(records)

# Generate data

hotel_records = generate_hotel_records_data()

# Write SQL files

write_sql_file("hotel_records.sql", hotel_records)
