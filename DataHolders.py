from datetime import datetime

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

    def __str__(self):
        return f"Seat: {self.seat}, Item: {self.item}, Allergy: {self.allergy}, Alteration: {self.alteration}"


class Order:
    def __init__(self, table, diningRoom, orders: list, time=None):
        self.time = time if time else datetime.now()
        self.table = table
        self.diningRoom = diningRoom
        self.orders = orders

    def add_order_item(self, orderitem: OrderItem):
        self.orders.append(orderitem)

    def remove_order_item(self, orderitem: OrderItem):
        self.orders = [item for item in self.orders if item != orderitem]  # Remove all occurrences of orderitem

    def __str__(self):
        orders_str = "\n".join(str(order) for order in self.orders)
        return f"Time: {self.time}, Table: {self.table}, Dining Room: {self.diningRoom}, Orders:\n{orders_str}"


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