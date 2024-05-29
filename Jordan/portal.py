from portal_interfaces import ITokenGuide, Portal
from login_portal import LoginPortal
from constants import TKeys
from user_token import User_Token
from ui import portal_ui_container, foh_ui_container
from functools import partial


class MainLoop:
    def __int__(self):
        pass


class MainPortal(ITokenGuide, Portal):
    """Main Portal, _portal is the current context"""

    def __init__(self, exit_func):
        self._exit = partial(exit_func[0], exit_func[1])
        self._token = None
        self._portal = None
        self.login()
        print('portal:', self._portal)
        print(self._token)
        from ui import portal_ui_container
        self._ui = portal_ui_container(self)

        while True:
            self._ui.user_in()

    def posses_token(self, user: 'User_Token'):
        self._token = user

    def guide_token(self, next_guide: ITokenGuide):
        next_guide.guide_token(self._token)

    def access_level(self) -> int:
        return 0

    def get_context(self) -> Portal:
        return self._portal

    def get_exit(self) -> partial:
        return self._exit

    def get_ui(self) -> portal_ui_container:
        return self._ui

    def login(self):
        print('logging in..')
        self._portal = LoginPortal(self)
        if self._portal.login():
            self._token: User_Token
            self._portal = self._token.data[TKeys.PortalKey]()
            print(self._portal)
            print("Login Successful")


class FOHPortal(Portal):
    def __init__(self):
        self._context = None
        self.set_context_dinning()
        self._ui = foh_ui_container(self)
        print('context:', self._context)

    def set_context_menu(self):
        self._context = Menu()

    def set_context_dinning(self):
        from dinning_room import Dinning_Room
        self._context = Dinning_Room()

    def get_ui(self) -> foh_ui_container:
        return self._ui

    def get_context(self) -> Portal:
        print('context:', self._context)
        return self._context


from singleton import Singleton


class Menu(Portal):
    """holds the menu data for the session"""

    # TODO: create acl permissions for removing menu item during service or adding daily specials

    def __int__(self):
        from ui import menu_ui_container
        self.main_menu = None
        self.sides_menu = None
        self.cold_drinks_menu = None
        self.hot_drinks_menu = None
        self.dessert_menu = None
        self.menu = None
        self.ui = menu_ui_container(self)

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
