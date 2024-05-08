from Mediator import Mediator
from Manager import Manager
from DatabaseManager import DatabaseHandler
from Client import ServerAPI
import time

if __name__ == "__main__":
    # webserver url
    url = 'http://192.168.20.7:8000/api/endpoint'

    # Create an instance of the Mediator class
    mediator = Mediator()

    database_manager = DatabaseHandler(host="localhost",
                                       user="user1",
                                       password="password1",
                                       database="Temp",
                                       name="databaseManager")

    # Create Manager classes
    OrderManager = Manager(mediator, "orderManager")
    FOHPortal = Manager(mediator, "FOHPortal")
    BOHPortal = Manager(mediator, "BOHPortal")
    BusinessPortal = Manager(mediator, "BusinessPortal")
    webServerClient = ServerAPI(mediator=mediator, url=url, name="webServerClient")

    # Subscribe to the Mediator
    mediator.add_to_comms(database_manager.name, database_manager)
    mediator.add_to_comms(OrderManager.name, OrderManager)
    mediator.add_to_comms(FOHPortal.name, FOHPortal)
    mediator.add_to_comms(BOHPortal.name, BOHPortal)
    mediator.add_to_comms(BusinessPortal.name, BusinessPortal)
    mediator.add_to_comms(webServerClient.name, webServerClient)



    # Main loop of program
    while True:
        # connect to webserver for updates ##### Make sure webserver is running first
        webServerClient.run()
        mediator.send_messages()
        time.sleep(2)
