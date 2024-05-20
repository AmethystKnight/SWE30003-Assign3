from DatabaseManager import DatabaseManager
from datetime import datetime
import DataHolders

class SalesFacade:
    def __init__(self, db_manager=DatabaseManager('root', 'password', '127.0.0.1', 'CafeDB')):
        self.db_manager = db_manager
        self.orders = {}  # Dictionary to store orders keyed by table number

    def create_order(self, order):
        if order.table in self.orders:
            return f"Order for table {order.table} already exists."
        self.orders[order.table] = order
        return f"Order created for table {order.table}: {order}"

    def delete_order_item(self, table_number, seat_number, order_item):
        if table_number not in self.orders:
            return f"No order found for table {table_number}."
        order = self.orders[table_number]
        for item in order.orders:
            if item.item == order_item and item.seat == seat_number:
                order.orders.remove(item)
                return f"Deleted item {order_item} from table {table_number} seat {seat_number}."
        return f"Item {order_item} not found in order for table {table_number}."

    def delete_all_order_items(self, table_number):
        if table_number not in self.orders:
            return f"No order found for table {table_number}."
        self.orders.pop(table_number)
        return f"Deleted all items from table {table_number}."

    def add_order_item(self, table_number, order_item):
        if table_number not in self.orders:
            return f"No order found for table {table_number}."
        # new_item = DataHolders.OrderItem(*order_item)
        self.orders[table_number].orders.append(order_item)
        return f"Added item {order_item} to table {table_number}."

    def process_payment(self, table_number, payment_type, issue_receipt):
        if table_number not in self.orders:
            return f"No order found for table {table_number}."

        # Retrieve the order and prepare sales data
        order = self.orders.pop(table_number)
        sales = [(item.item, 1, item.allergy) for item in order.orders]  # Simplified assumption: quantity = 1

        # Call sell_items to write these items to the salesrecord database
        if self.sell_items(sales):
            receipt = f"Receipt for table {table_number}: {order}, Payment Type: {payment_type}"
            if issue_receipt:
                receipt += ", Receipt Issued"
            return receipt
        else:
            return f"Failed to process payment for table {table_number}."

    def sell_items(self, sales):
        for sale in sales:
            dish, quantity, allergen = sale
            if allergen:
                if self.db_manager.check_allergy(dish, allergen):
                    print(f"Error: {dish} contains {allergen}. Sale not processed.")
                    return False
            self.db_manager.add_sales_record(datetime.now(), dish, quantity)
            print(f"Sold {quantity} of {dish}")
        return True


if __name__ == "__main__":
    db_manager = DatabaseManager('root', 'password', '127.0.0.1', 'CafeDB')
    sales_facade = SalesFacade(db_manager)

    # Example usage for testing purposes
    order_1 = DataHolders.Order(
        table=1,
        diningRoom='front',
        orders=[
            DataHolders.OrderItem(1, 'Espresso', 'Soy', 'No Sugar'),
            DataHolders.OrderItem(2, 'Latte', None, 'Extra Hot')
        ]
    )

    print(sales_facade.create_order(order_1))
    print(sales_facade.add_order_item(1, (3, 'Cappuccino', None, 'No Foam')))
    print(sales_facade.delete_order_item(1, 2, 'Latte'))
    print(sales_facade.delete_all_order_items(1))
    print(sales_facade.process_payment(1, 'credit', True))

    db_manager.close()
