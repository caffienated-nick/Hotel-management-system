import mysql.connector
from mysql.connector import Error

# Connect to MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="root",  # Replace with your MySQL password
            database="hotel_management"  # Replace with your database name
        )
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

# Create table for room assignments if it doesn't exist
def create_table1():
    connection = create_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS room_assignments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_name VARCHAR(10) NOT NULL,
                name VARCHAR(50),
                address VARCHAR(100),
                date_of_checkin DATE,
                number_of_people INT,
                email VARCHAR(100),
                phone_no VARCHAR(20),
                extra_services BOOLEAN,
                accomodation_services BOOLEAN,
                events BOOLEAN,
                wellness BOOLEAN,
                pets BOOLEAN,
                private_dining BOOLEAN,
                occasion BOOLEAN,                                                                  
                adhaar_numbers TEXT
            );
            """)
            connection.commit()
        connection.close()

# Create table for hotel records if it doesn't exist
def create_table2():
    connection = create_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Food_records (
                id INT PRIMARY KEY,
                Total_bill DECIMAL(10, 2)                                            
                                                 
            );
            """)
            connection.commit()
        connection.close()
def create_table3():
    connection = create_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice_table (
                id INT PRIMARY KEY,
                checkout_date DATE,
                days_stayed INT,
                final_bill DECIMAL(10, 2)                                                       
                                                 
            );
            """)            
            connection.commit()
        connection.close()
def create_combined_table():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS hotel_records (
                        id INT PRIMARY KEY,
                        room_name VARCHAR(10),
                        name VARCHAR(50),
                        address VARCHAR(100),
                        date_of_checkin DATE,
                        number_of_people INT,
                        email VARCHAR(100),
                        phone_no VARCHAR(20),
                        extra_services BOOLEAN,
                        accomodation_services BOOLEAN,
                        events BOOLEAN,
                        wellness BOOLEAN,
                        pets BOOLEAN,
                        private_dining BOOLEAN,
                        occasion BOOLEAN,
                        adhaar_numbers TEXT,
                        
                        checkout_date DATE,
                        days_stayed INT,
                        final_bill DECIMAL(10, 2)
                    );
                """)
                connection.commit()
                
        except Error as e:
            print(f"Error creating combined table: '{e}'")
        finally:
            connection.close()

# Insert a new room assignment record
def insert_combined(data):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO hotel_records 
                
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(query, data)
                connection.commit()
        except Error as e:
            print(f"Error inserting assignment: '{e}'")
        finally:
            connection.close()

def insert_invoice(data):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO invoice_table 
                (id, checkout_date, days_stayed, final_bill)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(query, data)
                connection.commit()
        except Error as e:
            print(f"Error inserting invoice: '{e}'")
        finally:
            connection.close()
def insert_assignment(data):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO room_assignments 
                (room_name, name, address, date_of_checkin, number_of_people, email, phone_no, extra_services, 
                 accomodation_services, events, wellness, pets, private_dining, occasion, adhaar_numbers)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(query, data)
                connection.commit()
        except Error as e:
            print(f"Error inserting assignment: '{e}'")
        finally:
            connection.close()
# Insert a new hotel record, such as food or stay data
def insert_fooddata(room_id, new_total_bill):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO Food_records (id, Total_bill)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                Total_bill = Total_bill + VALUES(Total_bill);
                """
                cursor.execute(query, (room_id, new_total_bill))
                connection.commit()
                
        except Error as e:
            print(f"Error upserting total bill: '{e}'")
        finally:
            connection.close()



# Retrieve the latest room assignment for a room
def get_latest_assignment(room_name):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT * FROM room_assignments 
                WHERE room_name = %s 
                ORDER BY id DESC 
                LIMIT 1;
                """
                cursor.execute(query, (room_name,))
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving latest assignment: '{e}'")
        finally:
            connection.close()
    return None
def get_fooddata(room_name):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT * FROM Food_records 
                WHERE id = %s ;
                
                """
                cursor.execute(query, (room_name,))
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving latest fooddata: '{e}'")
        finally:
            connection.close()
    return None
# Retrieve the latest hotel record for a room

def total_bookings():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT COUNT(id) AS total_bookings FROM room_assignments;
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving total bookings: '{e}'")
        finally:
            connection.close()
    return None
def total_no_of_people():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT SUM(number_of_people) AS tnop FROM room_assignments;
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving total no of people: '{e}'")
        finally:
            connection.close()
    return None

def total_extra_services():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT count(extra_services) AS tes FROM room_assignments WHERE extra_services = 1;
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving total no of people: '{e}'")
        finally:
            connection.close()
    return None

def total_accomodation_services():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT count(accomodation_services) AS tes FROM room_assignments WHERE accomodation_services = 1;
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving total no of people: '{e}'")
        finally:
            connection.close()
    return None
def total_events():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT count(events) AS tes FROM room_assignments WHERE events = 1;
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving total no of people: '{e}'")
        finally:
            connection.close()
    return None

def total_wellness():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT count(wellness) AS tes FROM room_assignments WHERE wellness = 1;
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving total no of people: '{e}'")
        finally:
            connection.close()
    return None
def total_pets():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT count(pets) AS tes FROM room_assignments WHERE pets = 1;
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving total no of people: '{e}'")
        finally:
            connection.close()
    return None
def total_private_dining():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT count(private_dining) AS tes FROM room_assignments WHERE private_dining = 1;
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving total no of people: '{e}'")
        finally:
            connection.close()
    return None
def total_occasion():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT count(occasion) AS tes FROM room_assignments WHERE occasion = 1;
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        except Error as e:
            print(f"Error retrieving total no of people: '{e}'")
        finally:
            connection.close()
    return None

def total_each_room():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                query = """
                SELECT room_name, COUNT(id) AS total_bookings FROM room_assignments GROUP BY room_name;
                """
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Error as e:
            print(f"Error retrieving total each room: '{e}'")
        finally:
            connection.close()
    return None 

def get_monthly_revenue():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                # Query to get monthly revenue
                query = """
                SELECT 
                    DATE_FORMAT(checkout_date, '%Y-%m') AS date, 
                    SUM(final_bill) AS revenue
                FROM 
                    hotel_records
                GROUP BY 
                    DATE_FORMAT(checkout_date, '%Y-%m')
                ORDER BY 
                    DATE_FORMAT(checkout_date, '%Y-%m');
                """
                cursor.execute(query)
                results = cursor.fetchall()
                
                # Format results in the desired dictionary format
                data = {
                    'data': [row['date'] for row in results],
                    'revenue': [float(row['revenue']) for row in results]
                }
                return data
        except Error as e:
            print(f"Error retrieving monthly revenue: '{e}'")
        finally:
            connection.close()
    return None
