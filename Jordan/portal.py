from portal_interfaces import ITokenGuide,Portal
from login_portal import LoginPortal
from constants import TKeys
from user_token import User_Token
from ui import portal_ui_container, foh_ui_container
from functools import partial

class MainLoop:
    def __int__(self):
        pass

class MainPortal(ITokenGuide,Portal):
    """Main Portal, _portal is the current context"""

    def __init__(self, exit_func):
        self._exit = partial(exit_func[0], exit_func[1])
        self._token = None
        self._portal = None
        from ui import portal_ui_container
        self._ui = portal_ui_container(self)
        # self._ui = {'main': portal_ui_container}
        # self.portal_commands = {'help': partial(self._ui['main'].print_help, self.portal_commands),
        #                         'login': self.login,
        #                         'exit': self._exit}
        self.login()
        # main loop
        while True:
            self._ui.user_in()

    #     while True:
    #         user_in = input("type help for commands")
    #         if user_in in self.portal_commands:
    #             self.portal_commands.get(user_in)()
    #         else:
    #             print('invalid input')
    #
    # def _print_help(self):
    #     for key in self.portal_commands.keys():
    #         print(key)

    def posses_token(self, user: 'User_Token'):
        self._token = user

    def guide_token(self, next_guide: ITokenGuide):
        next_guide.guide_token(self._token)

    def access_level(self) -> int:
        return 0

    def get_portal(self) -> vars:
        return self._portal
    def get_exit(self) -> partial:
        return self._exit

    def login(self):
        print('logging in..')
        self._portal = LoginPortal(self)
        if self._portal.login():
            self._token: User_Token
            self._portal = self._token.data[TKeys.PortalKey]()
            print("Login Successful")


class FOHPortal(Portal):
    def __init__(self, main_portal):
        from ui import foh_ui_container

        # self.portal_commands = {'menu': partial(self._ui['main'].print_help, self.portal_commands),
        #                         'dinning_room': self.login,
        #                         'orders': self._exit}
        # print("Front of House Portal Access")
        # self.parent = main_portal
        # self.parent.ui.context = foh_ui_container()
        self._ui = foh_ui_container()
        self.context = self.set_context_dinning()

    def set_context_menu(self):
        self.context = Menu()

    def set_context_dinning(self):
        from dinning_room import Dinning_Room
        self.context = Dinning_Room()

    def get_ui(self) -> foh_ui_container:
        return self._ui


from singleton import Singleton


class Menu(Portal):
    """holds the menu data for the session"""
    #TODO: create acl permissions for removing menu item during service or adding daily specials

    def __int__(self):
        self.main_menu = None
        self.sides_menu = None
        self.cold_drinks_menu = None
        self.hot_drinks_menu = None
        self.dessert_menu = None
        self.menu = None
        self.ui =

    def load_menu(self, token: 'User_Token', token_guide: 'ITokenGuide'):
        """since menuDB facade needs permissions, we need to use it, exit it,
        and then return the token back to its origin.
        Initially the menu will be loaded and then maybe updated via this method for
        menu updates like no more stock."""
        from facades import Facade_Menu_DB
        menu_db = Facade_Menu_DB()
        menu_db.posses_token(token)
        self.main_menu = menu_db.get_main_food_menu()
        self.sides_menu = menu_db.get_side_food_menu()
        self.cold_drinks_menu = menu_db.get_cold_drinks_menu()
        self.hot_drinks_menu = menu_db.get_hot_drinks_menu()
        self.dessert_menu = menu_db.get_side_dessert_menu()
        self.menu = self.main_menu.copy()
        self.menu.update(self.sides_menu)
        self.menu.update(self.cold_drinks_menu)
        self.menu.update(self.hot_drinks_menu)
        self.menu.update(self.dessert_menu)

    def get_item(self, name: str) -> dict:
        """gets a copy"""
        try:
            return self.menu[name].copy()
        except KeyError:
            print('item does not exist @ Menu -> get_item')
            return {}



class BOHPortal(Portal):
    def __init__(self):
        print("Back of House Portal Access")
        # TODO: add functionality


class BusinessPortal(Portal):
    def __init__(self):
        print("Business Portal Access")
        # TODO: add functionality
