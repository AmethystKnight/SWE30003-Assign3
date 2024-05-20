from OrderManager import OrderManager
import Portal as mg
from DatabaseManager import DatabaseManager

import time

if __name__ == "__main__":
    # webserver url
    url = 'http://192.168.20.7:8000/api/endpoint'

    # Create an instance of the Mediator class
    mediator = OrderManager()

    OrderManager = mg.OrderManager(mediator, "orderManager")
    FOHPortal = mg.FOHManager(mediator, "FOHPortal")
    BOHPortal = mg.BOHPortal(mediator, "BOHPortal")
    BusinessPortal = mg.BusinessPortal(mediator, "BusinessPortal")

    # Subscribe to the Mediator
    mediator.add_to_comms(OrderManager.name, OrderManager)
    mediator.add_to_comms(FOHPortal.name, FOHPortal)
    mediator.add_to_comms(BOHPortal.name, BOHPortal)
    mediator.add_to_comms(BusinessPortal.name, BusinessPortal)


    # Main loop of program
    while True:
        # I think here we should be call OrderManger.Run and it should be responsible for starting the system running.
        mediator.send_messages()
        time.sleep(2)


