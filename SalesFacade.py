from DatabaseManager import CafeDatabaseManager
from datetime import datetime

class CafeSalesFacade:
    def __init__(self, db_manager):
        self.db_manager = db_manager

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
    db_manager = CafeDatabaseManager('root', 'password', '127.0.0.1', 'CafeDB')
    sales_facade = CafeSalesFacade(db_manager)

    # Example sales
    sales = [
        ('Espresso', 1, 'Soy'),  # This should fail if Espresso contains Soy
        ('Espresso', 1, None)    # This should succeed
    ]

    result = sales_facade.sell_items(sales)
    if result:
        print("Sales processed successfully.")
    else:
        print("Sales processing failed.")

    db_manager.close()
