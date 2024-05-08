from msg import message

class Manager:
    def __init__(self, mediator, name):
        self.mediator = mediator
        self.data = None
        self.stats = None
        self.name = name

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




############################################################################
########################## CHILD CLASSES BELOW #############################
############################################################################



class FOHManager(Manager):
    def process_data(self):
        print(f"{self.name} has received the following data: \n {self.data}")

############################################################################
class OrderManager(Manager):
    def process_data(self):
        print(f"{self.name} has received the following data: \n {self.data}")


############################################################################
class BOHManager(Manager):
    def __init__(self, mediator, name):
        super().__init__(mediator, name)
        self.orderList = None

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

############################################################################
class BusinessPortal(Manager):
    def process_data(self):
        print(f"{self.name} has received the following data: \n {self.data}")