from Mediator import Mediator
import Manager as mg
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
    OrderManager = mg.OrderManager(mediator, "orderManager")
    FOHPortal = mg.FOHManager(mediator, "FOHPortal")
    BOHPortal = mg.BOHPortal(mediator, "BOHPortal")
    BusinessPortal = mg.BusinessPortal(mediator, "BusinessPortal")
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
        # I think here we should be call OrderManger.Run and it should be responsible for starting the system running.

        # connect to webserver for updates ##### Make sure webserver is running first
        webServerClient.run()
        mediator.send_messages()
        time.sleep(2)
