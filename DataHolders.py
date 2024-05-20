class Customer:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

class OrderItem:
    def __init__(self, seat, item, allergy, alteration):
        self.seat = seat
        self.item = item
        self.allergy = allergy
        self.alteration = alteration

class Order:
    def __init__(self, time, table, diningRoom, orders: list):
        self.time = time
        self.table = table
        self.diningRoom = diningRoom
        self.orders = orders

class Table:
    def __init__(self):
        pass

class DiningRoom:
    def __init__(self):
        pass

class Receipt:
    def __init__(self):
        pass

class Reservation:
    def __init__(self):
        pass