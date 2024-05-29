from Jordan.login_portal import LoginPortal
from functools import partial
from portal_interfaces import Portal
from abc import ABC


class ui_container(ABC):
    # TODO:Make a parent class for ui_container
    pass


# 'help': partial(self.print_help, self.portal_commands),
class portal_ui_container(ui_container):
    """Consider using MVC pattern:
    https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller"""

    def __init__(self, portal_data: 'MainPortal'):
        self.portal_data: Portal = portal_data
        print(self.portal_data)
        self.child_container: ui_container = portal_data.get_context().get_ui()
        self.portal_commands = {}
        self.portal_commands = \
            {'login': self.portal_data.login,
             'exit': self.portal_data.get_exit()}
        self.ui_template = \
            {'header': '------Kozy Koala App--------',
             'command_list': 'type: login, exit',
             'context': self.child_container.ui_template,
             'footer': '-----------------------------'}
        self.current_commands = None
        self.current_ui = None
        self.set_ui()
        self.set_portal_commands()
        self.print_ui()

    def print_ui(self):
        print()
        print()
        print()
        print(self.ui_template['header'])
        self.recursive_print(self.current_ui['command_list'])
        self.recursive_print(self.current_ui['context'])
        print(self.ui_template['footer'])

    def recursive_print(self, context):
        if isinstance(context, dict):
            for key, value in context.items():
                if isinstance(value, dict):
                    self.recursive_print(value)
                else:
                    print(value)
        else:
            print(context)

    def user_in(self):
        """main entry point and printer"""
        _in = input("type a command")
        if _in == 'p':
            self.print_ui()
        try:
            self.current_commands[_in]()
            print(self.ui_template)
        except KeyError:
            print('invalid input')
            self.user_in()
        self.set_portal_commands()
        self.set_ui()
        self.print_ui()

    def set_portal_commands(self):
        """Sets the current context's portal commands"""
        current_commands = self.portal_commands.copy()
        container: ui_container = self.child_container
        while container:
            try:
                current_commands.update(container.portal_commands)
            except AttributeError:
                break
            try:
                container = container.child_container
            except AttributeError:
                break
        self.current_commands = current_commands

    def set_ui(self):
        """sets the current contexts portal commands"""
        #TODO: change container.portal_commands to ui_template
        current_template = self.ui_template
        container: ui_container = self.child_container
        while container:
            try:
                current_template.update(container.portal_commands)
            except AttributeError:
                break
            try:
                container = container.child_container
            except AttributeError:
                break
        self.current_ui = current_template


    def print_help(self, portal_commands):
        print(self.ui_template['header'])
        for key in portal_commands.keys():
            print(key)
        print(self.ui_template['footer'])


class foh_ui_container(ui_container):
    def __init__(self, foh_data: 'FOHPortal'):
        self.foh_data = foh_data
        self.portal_commands = {
            'menu': self.set_context_menu,
            'dinning': self.set_context_dinning
        }
        self.ui_template = {
            'header': '---Front of House Portal---',
            'command_list': 'type: menu, dinning',
            'context': {},
            'footer': '-----------------------------'
        }
        self.child_container: ui_container = None
        self.set_context_dinning()
        print('Front of House Portal: access granted')

    def set_context_menu(self):
        self.foh_data.set_context_menu()
        self.child_container = self.foh_data.get_context().get_ui()
        self.update_ui()

    def set_context_dinning(self):
        self.foh_data.set_context_dinning()
        self.child_container = self.foh_data.get_context().get_ui()
        self.update_ui()

    def update_ui(self):
        if hasattr(self.child_container, 'ui_template'):
            self.ui_template['context'].update(self.child_container.ui_template['context'])



class dinning_room_ui_container(ui_container):
    def __init__(self, dinning_room: 'Dinning_Room'):
        self.dinning_room_data = dinning_room
        self.tables = self.dinning_room_data.get_all_tables_basic()
        self.portal_commands = {
            table[0]: self.create_table_command(table[0].split('_')[1])
            for table in self.tables
        }
        self.ui_template = {
            'header': '-----Select Table Number-----',
            'context': {table[0]: table for table in self.tables},
            'footer': '-----------------------------'
        }
    def create_table_command(self, table_number):
        def command():
            print(f"Selected Table_{table_number}")
        return command

class menu_ui_container(ui_container):
    def __init__(self, menu: 'Menu'):
        self.menu_data = menu
        self.portal_commands = {
            'main': self.show_main_menu,
            'sides': self.show_sides_menu,
            'cold_drinks': self.show_cold_drinks_menu,
            'hot_drinks': self.show_hot_drinks_menu,
            'desserts': self.show_dessert_menu
        }
        self.ui_template = {
            'header': '------Menu--------',
            'command_list': 'type: main, sides, cold_drinks, hot_drinks, desserts',
            'context': {},
            'footer': '-----------------------------'
        }
        self.set_ui('main_menu')

    def set_ui(self, menu_type: str):
        """Sets the current context's UI template based on the menu type."""
        menu_mapping = {
            'main_menu': self.menu_data.main_menu,
            'sides_menu': self.menu_data.sides_menu,
            'cold_drinks_menu': self.menu_data.cold_drinks_menu,
            'hot_drinks_menu': self.menu_data.hot_drinks_menu,
            'dessert_menu': self.menu_data.dessert_menu
        }
        menu = menu_mapping.get(menu_type, {})
        print('main menu',self.menu_data.main_menu)
        # self.ui_template['context'] = menu if menu else {}

    def show_main_menu(self):
        print(self.menu_data.main_menu)
        #
        # self.set_ui('main_menu')
        # self.print_ui()

    def show_sides_menu(self):
        print(self.menu_data.sides_menu)
        #
        # self.set_ui('sides_menu')
        # self.print_ui()

    def show_cold_drinks_menu(self):
        self.set_ui('cold_drinks_menu')
        print(self.menu_data.cold_drinks_menu)
        self.print_ui()

    def show_hot_drinks_menu(self):
        self.set_ui('hot_drinks_menu')
        print(self.menu_data.hot_drinks_menu)
        self.print_ui()

    def show_dessert_menu(self):
        self.set_ui('dessert_menu')
        print(self.menu_data.dessert_menu)
        self.print_ui()

    def print_ui(self):
        print("\n\n\n")
        print(self.ui_template['header'])
        print(self.ui_template['command_list'])
        self.recursive_print(self.ui_template['context'])
        print(self.ui_template['footer'])

    def recursive_print(self, context, indent=0):
        if isinstance(context, dict):
            for key, value in context.items():
                print(" " * indent + f"{key}:")
                if isinstance(value, dict):
                    self.recursive_print(value, indent + 2)
                else:
                    print(" " * (indent + 2) + str(value))
        else:
            print(" " * indent + str(context))
