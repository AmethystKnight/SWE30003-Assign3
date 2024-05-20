import tkinter as tk
from tkinter import messagebox
from ManagementFacade import ManagementFacade
from DatabaseManager import DatabaseManager
from datetime import datetime
from Manager import Manager
class BusinessPortal(Manager):
    def __init__(self, root, facade):
        self.facade = facade

        self.root = root
        self.root.title("Business Portal")
        self.root.geometry("400x600")

        # Create and place the widgets
        self.create_widgets()

    def process_data(self):
        print(f"{self.name} has received the following data: \n {self.data}")

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

        # Label and entry for getting sales records by date range
        self.date_range_label = tk.Label(self.root, text="Get Sales Records by Date Range")
        self.date_range_label.pack()

        self.start_date_label = tk.Label(self.root, text="Start Date (YYYY-MM-DD)")
        self.start_date_label.pack()
        self.start_date_entry = tk.Entry(self.root)
        self.start_date_entry.pack()

        self.end_date_label = tk.Label(self.root, text="End Date (YYYY-MM-DD)")
        self.end_date_label.pack()
        self.end_date_entry = tk.Entry(self.root)
        self.end_date_entry.pack()

        self.date_range_button = tk.Button(self.root, text="Get Sales Records", command=self.get_sales_records_by_date_range)
        self.date_range_button.pack()

        # Text box for displaying results
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack()

    def get_sales_records_by_date_range(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not self.validate_date_format(start_date) or not self.validate_date_format(end_date):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        sales = self.facade.get_sales_records_by_date_range(start_date, end_date)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Sales Records from {start_date} to {end_date}:\n")
        for sale in sales:
            self.result_text.insert(tk.END, f"{sale}\n")

    def validate_date_format(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def get_yesterdays_sales(self):
        sales = self.facade.get_yesterdays_sales()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Yesterday's Sales:\n")
        for sale in sales:
            self.result_text.insert(tk.END, f"{sale}\n")

    def add_menu_item(self):
        name = self.name_entry.get().strip()
        allergy = self.allergy_entry.get().strip()
        cost = self.cost_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return
        if not allergy:
            messagebox.showerror("Error", "Allergy information cannot be empty.")
            return
        try:
            cost = float(cost)
            if cost <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid cost. Please enter a positive number.")
            return

        self.facade.add_menu_item(name, allergy, cost)
        messagebox.showinfo("Success", f"Added {name} to the menu.")

    def delete_menu_item(self):
        name = self.delete_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return

        self.facade.delete_menu_item(name)
        messagebox.showinfo("Success", f"Deleted {name} from the menu.")

    def get_menu(self):
        menu = self.facade.get_menu()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Menu:\n")
        for item in menu:
            self.result_text.insert(tk.END, f"{item}\n")

if __name__ == "__main__":
    db_manager = DatabaseManager('root', 'password', '127.0.0.1', 'CafeDB')
    management_facade = ManagementFacade(db_manager)

    root = tk.Tk()
    portal = BusinessPortal(root, management_facade)
    root.mainloop()

    db_manager.close()
