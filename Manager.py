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


