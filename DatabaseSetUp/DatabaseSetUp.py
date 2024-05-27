import mysql.connector
from mysql.connector import errorcode
import subprocess
import sys
import os


# Function to install packages
def install_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


# Function to check if MariaDB is installed
def is_mariadb_installed():
    try:
        subprocess.check_call(['mariadb', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


# Function to install MariaDB
def install_mariadb():
    try:
        subprocess.check_call(['sudo', 'apt-get', 'update'])
        subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'mariadb-server'])
        subprocess.check_call(['sudo', 'service', 'mysql', 'start'])
        print("MariaDB installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install MariaDB: {e}")
        sys.exit(1)


# Install required packages
install_packages()

# Check if MariaDB is installed
if not is_mariadb_installed():
    print("MariaDB is not installed. Installing MariaDB...")
    install_mariadb()
else:
    print("MariaDB is already installed.")

# Database configuration
db_config = {
    'user': 'root',
    'password': 'password',  # Replace with your MariaDB root password
    'host': '127.0.0.1',
    'database': 'CafeDB'
}

# Connect to MariaDB
try:
    conn = mysql.connector.connect(
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host']
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create 'menu' table
    create_menu_table = """
    CREATE TABLE IF NOT EXISTS menu (
        Name VARCHAR(255),
        Allergy VARCHAR(255),
        Cost DECIMAL(10, 2)
    )
    """
    cursor.execute(create_menu_table)

    # Insert data into 'menu' table
    menu_items = [
        ('Espresso', 'None', 4.50),
        ('Cappuccino', 'None', 5.00),
        ('Latte', 'None', 4.50),
        ('Mocha', 'None', 4.75),
        ('Tea', 'None', 4.00),
        ('Hot Chocolate', 'Dairy', 5.00),
        ('Muffin', 'Gluten', 7.75),
        ('Croissant', 'Gluten', 6.25),
        ('Sandwich', 'Gluten', 12.50),
        ('Salad', 'None', 13.75)
    ]

    insert_menu_item = """
    INSERT INTO menu (Name, Allergy, Cost) 
    VALUES (%s, %s, %s)
    """
    cursor.executemany(insert_menu_item, menu_items)

    # Create 'salesRecord' table
    create_sales_record_table = """
    CREATE TABLE IF NOT EXISTS salesRecord (
        datetime DATETIME,
        Dish VARCHAR(255),
        Number_Sold INT
    )
    """
    cursor.execute(create_sales_record_table)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database and tables created successfully.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if conn.is_connected():
        conn.close()
