from Manager import Manager
class OrderManager(Manager):
    def process_data(self):
        print(f"{self.name} has received the following data: \n {self.data}")