import tkinter as tk
from tkinter import messagebox
from ManagementFacade import CafeManagementFacade
from DatabaseManager import CafeDatabaseManager


class BusinessPortal:
    def __init__(self, root, facade):
        self.facade = facade

        self.root = root
        self.root.title("Business Portal")
        self.root.geometry("400x400")

        # Create and place the widgets
        self.create_widgets()

    def create_widgets(self):
        # Label and button for getting yesterday's sales
        self.sales_label = tk.Label(self.root, text="Get Yesterday's Sales")
        self.sales_label.pack()
        self.sales_button = tk.Button(self.root, text="Get Sales", command=self.get_yesterdays_sales)
        self.sales_button.pack()

        # Label and entry for adding a new menu item
        self.add_label = tk.Label(self.root, text="Add Menu Item")
        self.add_label.pack()

        self.name_label = tk.Label(self.root, text="Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.allergy_label = tk.Label(self.root, text="Allergy")
        self.allergy_label.pack()
        self.allergy_entry = tk.Entry(self.root)
        self.allergy_entry.pack()

        self.cost_label = tk.Label(self.root, text="Cost")
        self.cost_label.pack()
        self.cost_entry = tk.Entry(self.root)
        self.cost_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_menu_item)
        self.add_button.pack()

        # Label and entry for deleting a menu item
        self.delete_label = tk.Label(self.root, text="Delete Menu Item")
        self.delete_label.pack()

        self.delete_name_label = tk.Label(self.root, text="Name")
        self.delete_name_label.pack()
        self.delete_name_entry = tk.Entry(self.root)
        self.delete_name_entry.pack()

        self.delete_button = tk.Button(self.root, text="Delete Item", command=self.delete_menu_item)
        self.delete_button.pack()

        # Label and button for getting the entire menu
        self.menu_label = tk.Label(self.root, text="Get Entire Menu")
        self.menu_label.pack()
        self.menu_button = tk.Button(self.root, text="Get Menu", command=self.get_menu)
        self.menu_button.pack()

        # Text box for displaying results
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack()

    def get_yesterdays_sales(self):
        sales = self.facade.get_yesterdays_sales()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Yesterday's Sales:\n")
        for sale in sales:
            self.result_text.insert(tk.END, f"{sale}\n")

    def add_menu_item(self):
        name = self.name_entry.get()
        allergy = self.allergy_entry.get()
        cost = self.cost_entry.get()
        try:
            self.facade.add_menu_item(name, allergy, float(cost))
            messagebox.showinfo("Success", f"Added {name} to the menu.")
        except ValueError:
            messagebox.showerror("Error", "Invalid cost. Please enter a number.")

    def delete_menu_item(self):
        name = self.delete_name_entry.get()
        self.facade.delete_menu_item(name)
        messagebox.showinfo("Success", f"Deleted {name} from the menu.")

    def get_menu(self):
        menu = self.facade.get_menu()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Menu:\n")
        for item in menu:
            self.result_text.insert(tk.END, f"{item}\n")


if __name__ == "__main__":
    db_manager = CafeDatabaseManager('root', 'password', '127.0.0.1', 'CafeDB')
    management_facade = CafeManagementFacade(db_manager)

    root = tk.Tk()
    portal = BusinessPortal(root, management_facade)
    root.mainloop()

    db_manager.close()
