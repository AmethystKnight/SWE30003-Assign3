from singleton import Singleton
from portal_interfaces import ITokenGuide
import pytz
from datetime import datetime

class Table:
    def __init__(self, table_id, capacity):
        self.table_id = table_id
        self.capacity = capacity

def get_tz():
    return pytz.timezone('Australia/Melbourne')

class Facade_DB(Singleton, ITokenGuide):
    def __init__(self):
        self._context = None
        self._token = None
        self._access = 1

    def posses_token(self, token: 'User_Token'):
        """ACL is used to help give permissions"""
        from acl import ACL
        acl = ACL()
        acl.posses_token(token)
        if acl.guide_token(self):
            self._context = self.create_crud_context()
            print('accessed DB with CRUD permissions')
        else:
            self._access = 0
            if acl.guide_token(self):
                print('accessed DB')
                self._access = 1
            else:
                print('DB, bad permissions')
                exit()

    def guide_token(self, next_guide: 'ITokenGuide'):
        self._context = None
        next_guide.posses_token(self._token)
        self._token = None

    def access_level(self) -> int:
        """Integers are immutable in Python"""
        return self._access

    def create_crud_context(self):
        raise NotImplementedError("Subclasses should implement this method")

class Facade_Menu_DB(Facade_DB):
    """Would use a DB with a table for each menu type or one table
    that would have a label for each sub-menu type: hot drinks, cold drinks,
    main menu, side menu, desserts
    https://allergyfacts.org.au/resources/food-allergen-cards
    Allergens are retrieved from a look-up table and are compiled into,
    the allergy section as list.
    Full CRUD permissions could be given to a token via ACL, such as logging into
    business portal """

    def create_crud_context(self):
        return _Facade_Menu_DB_CRUD()

    def get_hot_drinks_menu(self) -> dict:
        drinks = {
            'espresso': {'item': 'espresso', 'allergy': None, 'cost': 4.00},
            'latte': {'item': 'latte', 'allergy': ['lactose'], 'cost': 4.50},
            'chai_latte': {'item': 'chai latte', 'allergy': ['lactose'], 'cost': 6.50},
        }
        return drinks

    def get_cold_drinks_menu(self) -> dict:
        drinks = {
            'juice': {'item': 'juice', 'allergy': None, 'cost': 4.50},
            'beer': {'item': 'beer', 'allergy': None, 'cost': 8.50},
            'wine': {'item': 'wine', 'allergy': None, 'cost': 12.50},
        }
        return drinks

    def get_main_food_menu(self) -> dict:
        menu = {
            'eggs_bacon': {'item': 'eggs and bacon on toast', 'allergy': ['egg', 'gluten'], 'cost': 13.50},
            'beans_toast': {'item': 'beans and toast', 'allergy': ['gluten'], 'cost': 10.50},
            'steak_sandwich': {'item': 'steak sandwich', 'allergy': None, 'cost': 21.50},
            'pumpkin_salad': {'item': 'pumpkin salad', 'allergy': ['nuts'], 'cost': 18.50},
            'chicken_pie': {'item': 'chicken pie', 'allergy': None, 'cost': 11.50},
        }
        return menu

    def get_side_food_menu(self) -> dict:
        menu = {
            'garlic_bread': {'item': 'garlic bread', 'allergy': ['lactose'], 'cost': 8.00},
            'french_fries': {'item': 'french fries', 'allergy': None, 'cost': 8.50},
        }
        return menu

    def get_side_dessert_menu(self) -> dict:
        menu = {
            'cheese_cake': {'item': 'cheese cake', 'allergy': ['lactose'], 'cost': 9.00},
            'creme_brulee': {'item': 'creme brulee', 'allergy': ['egg', 'nuts'], 'cost': 8.50},
        }
        return menu

class _Facade_Menu_DB_CRUD(Singleton, ITokenGuide):
    """Class for full CRUD permissions for higher permissions"""
    def update_item(self):
        pass

    def delete_item(self):
        pass

    def add_item(self):
        pass

class Facade_Dinning_Room_DB(Facade_DB):
    def create_crud_context(self):
        return _Facade_Dinning_Room_DB_CRUD()

    def get_tables(self):
        """DB SCHEMA: {table number:int : table:Table}
        Data SCHEMA: {table number:int {table:string: table:Table, reservation:dict}}"""
        from dinning_room import Table
        tables = {
            1: Table(1, 4), 2: Table(2, 4), 3: Table(3, 4), 4: Table(4, 4),
            5: Table(5, 5), 6: Table(6, 5), 7: Table(7, 6), 8: Table(8, 6),
            9: Table(9, 6), 10: Table(10, 6), 11: Table(11, 8), 12: Table(12, 12)
        }
        # Returns the db data with reservation data embedded
        new_tables = {}
        for number, table in tables.items():
            new_tables[number] = {'table': table, 'reservation': self.get_reservation_template()}
        return new_tables

    def get_reservation_template(self):
        """SCHEMA: {time:string : [time:datetime, reserved:bool]}"""
        tz = get_tz()
        reservation_template = {
            '8:30am': [datetime.strptime('8:30am', '%I:%M%p').replace(tzinfo=tz), False],
            '9:00am': [datetime.strptime('9:00am', '%I:%M%p').replace(tzinfo=tz), False],
            '9:30am': [datetime.strptime('9:30am', '%I:%M%p').replace(tzinfo=tz), False],
            '10:00am': [datetime.strptime('10:00am', '%I:%M%p').replace(tzinfo=tz), False],
            '10:30am': [datetime.strptime('10:30am', '%I:%M%p').replace(tzinfo=tz), False],
            '11:00am': [datetime.strptime('11:00am', '%I:%M%p').replace(tzinfo=tz), False],
            '11:30am': [datetime.strptime('11:30am', '%I:%M%p').replace(tzinfo=tz), False],
            '12:00pm': [datetime.strptime('12:00pm', '%I:%M%p').replace(tzinfo=tz), False],
            '12:30pm': [datetime.strptime('12:30pm', '%I:%M%p').replace(tzinfo=tz), False],
            '1:00pm': [datetime.strptime('1:00pm', '%I:%M%p').replace(tzinfo=tz), False],
            '1:30pm': [datetime.strptime('1:30pm', '%I:%M%p').replace(tzinfo=tz), False],
            '2:00pm': [datetime.strptime('2:00pm', '%I:%M%p').replace(tzinfo=tz), False],
            '2:30pm': [datetime.strptime('2:30pm', '%I:%M%p').replace(tzinfo=tz), False],
            '3:00pm': [datetime.strptime('3:00pm', '%I:%M%p').replace(tzinfo=tz), False]
        }
        return reservation_template

class _Facade_Dinning_Room_DB_CRUD(Singleton, ITokenGuide):
    """Class for full CRUD permissions for higher permissions"""
    def update_item(self):
        pass

    def delete_item(self):
        pass

    def add_item(self):
        pass

# Example usage
facade_menu_db = Facade_Menu_DB()
print(facade_menu_db.get_hot_drinks_menu())

facade_dinning_room_db = Facade_Dinning_Room_DB()
tables_with_reservations = facade_dinning_room_db.get_tables()
for table_number, details in tables_with_reservations.items():
    print(f"Table {table_number}: {details}")
