import tkinter as tk
from tkinter import messagebox
from Display import Display
from SalesFacade import SalesFacade
import DataHolders

class FOHPortal(Display):
    def __init__(self, mediator, name, sales_facade):
        super().__init__(mediator, name)
        self.portal_window = None
        self.sales_facade = sales_facade

    def process_data(self):
        print(f"{self.name} has received the following data: \n {self.data}")

    def create_portal_widgets(self):
        # New Order Section
        new_order_frame = tk.LabelFrame(self.portal_window, text="New Order")
        new_order_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        tk.Label(new_order_frame, text="Table Number:").pack()
        self.new_order_table_number_entry = tk.Entry(new_order_frame)
        self.new_order_table_number_entry.pack()

        tk.Label(new_order_frame, text="Seat Number:").pack()
        self.new_order_seat_number_entry = tk.Entry(new_order_frame)
        self.new_order_seat_number_entry.pack()

        tk.Label(new_order_frame, text="Order Item:").pack()
        self.new_order_item_entry = tk.Entry(new_order_frame)
        self.new_order_item_entry.pack()

        tk.Label(new_order_frame, text="Allergy:").pack()
        self.new_order_allergy_entry = tk.Entry(new_order_frame)
        self.new_order_allergy_entry.pack()

        tk.Label(new_order_frame, text="Alterations:").pack()
        self.new_order_alterations_entry = tk.Entry(new_order_frame)
        self.new_order_alterations_entry.pack()

        self.add_order_item_button = tk.Button(new_order_frame, text="Add Order Item", command=self.add_order_item)
        self.add_order_item_button.pack()

        self.new_order_button = tk.Button(new_order_frame, text="Create New Order", command=self.create_new_order)
        self.new_order_button.pack()

        # Update Order Section
        update_order_frame = tk.LabelFrame(self.portal_window, text="Update Order")
        update_order_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        tk.Label(update_order_frame, text="Table Number:").pack()
        self.update_table_number_entry = tk.Entry(update_order_frame)
        self.update_table_number_entry.pack()

        tk.Label(update_order_frame, text="Order Item:").pack()
        self.update_order_item_entry = tk.Entry(update_order_frame)
        self.update_order_item_entry.pack()

        tk.Label(update_order_frame, text="Allergy:").pack()
        self.update_order_allergy_entry = tk.Entry(update_order_frame)
        self.update_order_allergy_entry.pack()

        tk.Label(update_order_frame, text="Alterations:").pack()
        self.update_order_alterations_entry = tk.Entry(update_order_frame)
        self.update_order_alterations_entry.pack()

        tk.Label(update_order_frame, text="Seat Number:").pack()
        self.update_seat_number_entry = tk.Entry(update_order_frame)
        self.update_seat_number_entry.pack()


        self.add_update_order_item_button = tk.Button(update_order_frame, text="Add Order Item", command=self.add_update_order_item)
        self.add_update_order_item_button.pack()

        self.delete_order_item_button = tk.Button(update_order_frame, text="Delete Order Item", command=self.delete_order_item)
        self.delete_order_item_button.pack()

        self.delete_all_button = tk.Button(update_order_frame, text="Delete All", command=self.delete_all_order_items)
        self.delete_all_button.pack()

        # Payment Section
        payment_frame = tk.LabelFrame(self.portal_window, text="Payment")
        payment_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        tk.Label(payment_frame, text="Table Number:").pack()
        self.payment_table_number_entry = tk.Entry(payment_frame)
        self.payment_table_number_entry.pack()

        tk.Label(payment_frame, text="Payment Type:").pack()

        self.payment_type = tk.StringVar(value="credit")
        tk.Radiobutton(payment_frame, text="Credit", variable=self.payment_type, value="credit").pack()
        tk.Radiobutton(payment_frame, text="Cash", variable=self.payment_type, value="cash").pack()
        tk.Radiobutton(payment_frame, text="EFTPOS", variable=self.payment_type, value="eftpos").pack()

        self.issue_receipt_var = tk.BooleanVar()
        self.issue_receipt_check = tk.Checkbutton(payment_frame, text="Issue Receipt", variable=self.issue_receipt_var)
        self.issue_receipt_check.pack()

        self.process_payment_button = tk.Button(payment_frame, text="Process Payment", command=self.process_payment)
        self.process_payment_button.pack()

        # Result Section
        self.result_text = tk.Text(self.portal_window, height=10, width=50)
        self.result_text.pack()
    def add_order_item(self):
        table_number = self.new_order_table_number_entry.get()
        seat_number = self.new_order_seat_number_entry.get()
        item = self.new_order_item_entry.get()
        allergy = self.new_order_allergy_entry.get()
        alterations = self.new_order_alterations_entry.get()

        if table_number not in self.sales_facade.orders:
            self.sales_facade.orders[table_number] = DataHolders.Order(table_number, "Main Dining", [])

        order_item = DataHolders.OrderItem(seat_number, item, allergy, alterations)

        item_added, return_str = self.sales_facade.add_order_item(table_number, order_item   )
        if item_added:
            self.result_text.insert(tk.END, f"Added item: {order_item}\n")
        else:
            self.result_text.insert(tk.END, f"{return_str}\n")
    def create_new_order(self):
        table_number = self.new_order_table_number_entry.get()
        if not table_number:
            messagebox.showerror("Input Error", "Table number is required")
            return

        if table_number not in self.sales_facade.orders:
            self.result_text.insert(tk.END, f"No order found for table {table_number}\n")
            return

        order = self.sales_facade.orders[table_number]
        self.send_order(order)
        self.result_text.insert(tk.END, f"Order sent for table {table_number}\n")

    def send_order(self, order):
        # Print order details for now
        print(order)

    def add_update_order_item(self):
        table_number = self.update_table_number_entry.get()
        if not table_number:
            messagebox.showerror("Input Error", "Table number is required")
            return

        seat_number = self.update_seat_number_entry.get()  # Get seat number input
        if not seat_number:
            messagebox.showerror("Input Error", "Seat number is required")
            return

        item = self.update_order_item_entry.get()
        allergy = self.update_order_allergy_entry.get()
        alterations = self.update_order_alterations_entry.get()

        if table_number not in self.sales_facade.orders:
            messagebox.showerror("Table Error", f"No order found for table {table_number}")
            return

        order_item = DataHolders.OrderItem(seat_number, item, allergy, alterations)
        self.sales_facade.add_order_item(table_number, order_item)
        self.result_text.insert(tk.END, f"Added item: {order_item}\n")

    def delete_order_item(self):
        table_number = self.update_table_number_entry.get()
        if not table_number:
            messagebox.showerror("Input Error", "Table number is required")
            return

        seat_number = self.update_seat_number_entry.get()  # Get seat number input
        if not seat_number:
            messagebox.showerror("Input Error", "Seat number is required")
            return

        order_item = self.update_order_item_entry.get()
        result = self.sales_facade.delete_order_item(table_number, seat_number, order_item)
        self.result_text.insert(tk.END, f"{result}\n")

    def delete_all_order_items(self):
        table_number = self.update_table_number_entry.get()
        if not table_number:
            messagebox.showerror("Input Error", "Table number is required")
            return

        if table_number not in self.sales_facade.orders:
            messagebox.showerror("Table Error", f"No order found for table {table_number}")
            return

        del self.sales_facade.orders[table_number]
        self.result_text.insert(tk.END, f"All order items deleted for table {table_number}\n")

    def process_payment(self):
        table_number = self.payment_table_number_entry.get()
        payment_type = self.payment_type.get()
        issue_receipt = self.issue_receipt_var.get()
        result = self.sales_facade.process_payment(table_number, payment_type, issue_receipt)
        self.result_text.insert(tk.END, f"{result}\n")

    def display_portal(self):
        if self.logged_in and not self.portal_window:
            self.portal_window = tk.Tk()
            self.portal_window.title("FOH Portal")
            self.portal_window.geometry("500x900")
            self.create_portal_widgets()
            self.portal_window.mainloop()


# For testing purposes
if __name__ == "__main__":

    sales_facade = SalesFacade()

    # Create a FOHPortal instance
    manager = FOHPortal(None, "FOH Portal", sales_facade)
    # Test the login functionality
    manager.start()

