import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, user, password, host, database):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Database connection established.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")

    def get_menu(self):
        query = "SELECT * FROM menu"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_item_by_name(self, name):
        query = "SELECT * FROM menu WHERE Name = %s"
        self.cursor.execute(query, (name,))
        return self.cursor.fetchone()

    def get_items_by_allergen(self, allergen):
        query = "SELECT * FROM menu WHERE Allergy = %s"
        self.cursor.execute(query, (allergen,))
        return self.cursor.fetchall()

    def get_items_without_allergen(self, allergen):
        query = "SELECT * FROM menu WHERE Allergy != %s"
        self.cursor.execute(query, (allergen,))
        return self.cursor.fetchall()

    def add_menu_item(self, name, allergy, cost):
        query = "INSERT INTO menu (Name, Allergy, Cost) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (name, allergy, cost))
        self.conn.commit()

    def delete_menu_item(self, name):
        query = "DELETE FROM menu WHERE Name = %s"
        self.cursor.execute(query, (name,))
        self.conn.commit()

    def update_menu_item_price(self, name, new_price):
        query = "UPDATE menu SET Cost = %s WHERE Name = %s"
        self.cursor.execute(query, (new_price, name))
        self.conn.commit()

    def add_sales_record(self, datetime, dish, number_sold):
        query = "INSERT INTO salesRecord (datetime, Dish, Number_Sold) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (datetime, dish, number_sold))
        self.conn.commit()

    def delete_sales_record_by_date_range(self, start_date, end_date):
        query = "DELETE FROM salesRecord WHERE datetime BETWEEN %s AND %s"
        self.cursor.execute(query, (start_date, end_date))
        self.conn.commit()

    def check_item_existence(self, name):
        query = "SELECT * FROM menu WHERE Name = %s"
        self.cursor.execute(query, (name,))
        return self.cursor.fetchone() is not None

    def check_allergy(self, dish, allergen):
        query = "SELECT * FROM menu WHERE Name = %s AND Allergy = %s"
        self.cursor.execute(query, (dish, allergen))
        return self.cursor.fetchone() is not None

    def get_yesterdays_sales(self):
        yesterday = datetime.now() - timedelta(days=1)
        start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = "SELECT * FROM salesrecord WHERE datetime BETWEEN %s AND %s"
        self.cursor.execute(query, (start_of_yesterday, end_of_yesterday))
        return self.cursor.fetchall()

    def get_sales_records_by_date_range(self, start_date, end_date):
        query = "SELECT * FROM salesRecord WHERE datetime BETWEEN %s AND %s"
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()


if __name__ == "__main__":
    # Example usage
    db_manager = DatabaseManager('root', 'password', '127.0.0.1', 'CafeDB')

    # Fetch entire menu
    menu = db_manager.get_menu()
    print("Entire Menu:", menu)

    # Fetch single item by name
    item = db_manager.get_item_by_name('Espresso')
    print("Espresso Item:", item)

    # Fetch items by allergen
    items_with_gluten = db_manager.get_items_by_allergen('Gluten')
    print("Items with Gluten:", items_with_gluten)

    # Fetch items without allergen
    items_without_dairy = db_manager.get_items_without_allergen('Dairy')
    print("Items without Dairy:", items_without_dairy)

    # Add new menu item
    db_manager.add_menu_item('Bagel', 'Gluten', 2.00)

    # Delete menu item
    db_manager.delete_menu_item('Bagel')
    item_name = 'Esppresso'
    if db_manager.check_item_existence(item_name):
        print(f"{item_name} exists in the menu.")
    else:
        print(f"{item_name} does not exist in the menu.")
    # Update menu item price
    db_manager.update_menu_item_price('Latte', 3.75)

    # Add sales record
    db_manager.add_sales_record('2024-05-18 10:30:00', 'Latte', 5)

    # Delete sales records by date range
    db_manager.delete_sales_record_by_date_range('2024-05-01', '2024-05-02')

    # Fetch yesterday's sales
    yesterdays_sales = db_manager.get_yesterdays_sales()
    print("Yesterday's Sales:", yesterdays_sales)

    db_manager.close()
