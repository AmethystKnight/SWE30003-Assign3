import requests
import json
from msg import message

class ServerAPI:
    def __init__(self, url, mediator, name):
        self.url = url
        self.mediator = mediator
        self.data = None
        self.name = name

    def send_to_mediator(self, msg):
        self.mediator.receive_message(msg)

    def receive_message(self, msg):
        channel = msg.get_channel()
        if channel == 'default':
            self.process_data()
        elif channel == 'other':
            pass
        else:
            pass

    def process_data(self):
        print(f"{self.name} has received the following data: \n {self.data}")

    def run(self):
        self.data = self.get_data()
        if self.data is not None and 'current_customers' in self.data:
            self.current_customers = self.data['current_customers']
            self.send_to_mediator(message('orderManager', data=self.current_customers))

    def get_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except json.decoder.JSONDecodeError:
                print('Empty or invalid JSON response received')
                return None
        else:
            print('Error:', response.status_code)
            return None



