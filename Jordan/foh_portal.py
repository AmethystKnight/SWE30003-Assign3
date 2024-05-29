from portal_interfaces import Portal
from functools import partial

class FOHPortal(Portal):
    def __init__(self, main_portal):
        from ui import FOHUIContainer

        self._ui = FOHUIContainer()
        self.parent = main_portal
        self.parent._ui._context = self._ui
        self.portal_commands = {
            'menu': partial(self._ui.print_help, self.portal_commands),
            'dinning_room': self.dinning_room,
            'orders': self.orders
        }

    def dinning_room(self):
        print("Accessing the dining room...")

    def orders(self):
        print("Managing orders...")
