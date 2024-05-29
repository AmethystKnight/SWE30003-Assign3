from datetime import datetime


class Order:
    """defined as a list of menu item names derived
    directly from the db"""

    def __int__(self, *args):
        self.order = args


class Table:
    def __init__(self, number: int, capacity: int):
        from invoice_manager import Invoice_Manager
        self.number = number
        self.capacity = capacity
        self.invoice_manager = Invoice_Manager()
        self.invoice = self.invoice_manager.get_next_invoice()
        self.order = []
        self.occupied = False

    def add_order(self, order):
        self.occupied = True

    def push_to_invoice_manager(self):
        self.occupied = False
        # TODO: add functionality
        pass


class Dinning_Room:
    """the table layout is expected to be managed through a db, they are relatively static,
    this should also be true for a reservation template.
    Tables SCHEMA: {table number:int {table:string: table:Table, reservation:dict}}"""

    def __init__(self):
        from invoice_manager import Invoice_Manager
        from facades import Facade_Dinning_Room_DB
        from helper_functions import get_current_time_in_melbourne
        from ui import dinning_room_ui_container
        dinning_db = Facade_Dinning_Room_DB()
        self._tables = dinning_db.get_tables()
        self._get_time = get_current_time_in_melbourne
        self._invoice_manager = Invoice_Manager()
        self._booking_reference = {table_number: table['reservation'] for table_number, table in self._tables.items()}
        self._ui = dinning_room_ui_container(self)

    def create_booking(self, table_number: int, time: str) -> bool:
        try:
            res = self._tables[table_number]['reservation'][time][1]
            if res is True or self._tables[table_number]['table'].occupied is True:
                return False
            else:
                res = True
                self._booking_reference[table_number][time] = res
                return True
        except KeyError:
            print('Key Error @ Dinning_Room -> create_booking')

    def free_table(self, table_number: int, time: str = None):
        from helper_functions import round_up_to_next_30_minutes
        if time is None:
            time = round_up_to_next_30_minutes(self._get_time()).strftime('%I:%M%p').lower()

        for t in self._booking_reference[table_number]:
            if datetime.strptime(t, '%I:%M%p') >= datetime.strptime(time, '%I:%M%p'):
                self._booking_reference[table_number][t][1] = False

    def get_all_tables_basic(self) -> list:
        """Returns all tables as a representation of their number formatted like: Table_n and reservation value."""
        tables = []
        for table_number, table_info in self._tables.items():
            reservation_status = any(reservation[1] for reservation in table_info['reservation'].values())
            tables.append(f"Table_{table_number}, {'Reserved' if reservation_status else 'Free'}")
        return tables

    def get_ui(self) -> 'dinning_room_ui_container':
        return self._ui

    def get_tables(self) -> dict:
        return self._tables

class Order_Manager:
    # TODO: add functionality
    pass