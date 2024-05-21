from DatabaseManager import DatabaseManager
class MenuFacade:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_menu(self, contains=None, allergy=None, columns=None):
        if contains is not None and allergy:
            if contains:
                result = self.db_manager.get_items_by_allergen(allergy)
            else:
                result = self.db_manager.get_items_without_allergen(allergy)
        else:
            result = self.db_manager.get_menu()

        if columns:
            result = self.filter_columns(result, columns)

        return result

    def filter_columns(self, rows, columns):
        return [[row[col - 1] for col in columns] for row in rows]


# Example usage:
if __name__ == "__main__":
    db_manager = DatabaseManager('root', 'password', '127.0.0.1', 'CafeDB')
    menu_facade = MenuFacade(db_manager)

    # Fetch entire menu
    print("Entire Menu:")
    menu = menu_facade.get_menu()
    for item in menu:
        print(item)

    # Fetch items with allergen
    print("\nItems with Gluten:")
    items_with_gluten = menu_facade.get_menu(contains=True, allergy='Gluten')
    for item in items_with_gluten:
        print(item)

    # Fetch items without allergen
    print("\nItems without Dairy:")
    items_without_dairy = menu_facade.get_menu(contains=False, allergy='Dairy')
    for item in items_without_dairy:
        print(item)

    # Fetch entire menu with specific columns (e.g., columns 1 and 3)
    print("\nMenu with Columns 1 and 3:")
    menu_columns_1_3 = menu_facade.get_menu(columns=(1, 3))
    for item in menu_columns_1_3:
        print(item)

    # Fetch items with allergen with specific columns (e.g., columns 2 and 3)
    print("\nItems with Gluten (Columns 2 and 3):")
    items_with_gluten_columns_2_3 = menu_facade.get_menu(contains=True, allergy='Gluten', columns=(2, 3))
    for item in items_with_gluten_columns_2_3:
        print(item)

    print("\nItems with Gluten (Columns 1 and 2):")
    items_with_gluten_columns_2_3 = menu_facade.get_menu(contains=True, allergy='Gluten', columns=(1, 2))
    for item in items_with_gluten_columns_2_3:
        print(item)

    print("\nItems with Gluten (Columns 1 and 1):")
    items_with_gluten_columns_2_3 = menu_facade.get_menu(contains=True, allergy='Gluten', columns=(1, 1))
    for item in items_with_gluten_columns_2_3:
        print(item)


    db_manager.close()
