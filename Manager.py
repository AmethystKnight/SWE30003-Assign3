import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

class Manager(ABC):
    def __init__(self, mediator, name):
        self.mediator = mediator
        self.data = None
        self.stats = None
        self.name = name
        self.logged_in = False  # Track login status

    def send_to_mediator(self, msg):
        self.mediator.receive_message(msg)

    def receive_message(self, msg):
        channel = msg.get_channel()
        if channel == 'default':
            self.data = msg.get_data()
            self.process_data()
        elif channel == 'channel1':
            pass
        else:
            # Handle other cases if needed
            pass

    def process_data(self):
        print(f"{self.name} has received the following data: \n {self.data}")

    def start(self):
        self.login()  # Start the login process
        if self.logged_in:
            self.display_portal()

    def login(self):
        def attempt_login():
            # Retrieve the entered username and password
            username = username_entry.get()
            password = password_entry.get()

            # Authentication logic goes here
            # Replace the following placeholder logic with actual authentication check
            if username == "admin" and password == "admin":  # Placeholder: replace with real check
                print("Login successful!")
                self.logged_in = True  # Set logged_in to True upon successful login
                login_window.destroy()  # Close the login window
            else:
                # Show an error message if login fails
                messagebox.showerror("Login Failed", "Invalid username or password")

        def on_closing():
            # Handle the window close event
            if messagebox.askokcancel("Quit", "Do you want to quit the login process?"):
                login_window.destroy()

        # Create the login window
        login_window = tk.Tk()
        login_window.title("Login")

        # Add labels and entry fields for username and password
        tk.Label(login_window, text="Username:").grid(row=0)
        tk.Label(login_window, text="Password:").grid(row=1)

        # Entry fields for username and password
        username_entry = tk.Entry(login_window)
        password_entry = tk.Entry(login_window, show="*")

        # Position the entry fields in the grid
        username_entry.grid(row=0, column=1)
        password_entry.grid(row=1, column=1)

        # Login button to trigger the attempt_login function
        login_button = tk.Button(login_window, text="Login", command=attempt_login)
        login_button.grid(row=2, column=1)

        # Handle window close event
        login_window.protocol("WM_DELETE_WINDOW", on_closing)
        login_window.mainloop()  # Use mainloop to handle window events

        return self.logged_in  # Return login status

    @abstractmethod
    def display_portal(self):
        pass


############################################################################
########################## CHILD CLASSES BELOW #############################
############################################################################

#class FOHPortal in front_of_house_portal.py
#class BusinessPortal in business_portal.py
class BOHPortal(Manager):
    def __init__(self, mediator, name):
        super().__init__(mediator, name)
        self.orderList = []

    def receive_message(self, msg):
        channel = msg.get_channel()
        if channel == 'default':
            self.data = msg.get_data()
            self.process_data()
        elif channel == 'newOrder':
            self.orderList.append(msg.get_data())
            self.process_data()
        else:
            # Handle other cases if needed
            pass

    def process_data(self):
        print(f"{self.name} has received the following data: \n {self.data}")

    def display_portal(self):
        if not hasattr(self, 'portal_window'):
            self.portal_window = tk.Tk()
            self.portal_window.title("BOH Portal")
            self.portal_window.geometry("200x200")  # Set window size to 200x200 pixels

            # Add label at the top
            tk.Label(self.portal_window, text="BOHPortal", font=("Helvetica", 16)).pack()

            self.portal_window.mainloop()


#  For testing purposes
if __name__ == "__main__":
    # Create a mediator instance
    mediator = None
    # Create a BOHManager instance
    manager = BOHPortal(mediator, "BOH Manager")
    # Test the login functionality
    manager.start()
