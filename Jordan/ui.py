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
        print(self.ui_template['command_list'])
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
        try:
            self.portal_commands[_in]()
            print(self.ui_template)
        except KeyError:
            print('invalid input')
            self.user_in()

    def set_portal_commands(self):
        """sets the current contexts portal commands"""
        current_commands = [self.portal_commands]
        container: ui_container = self.child_container
        while container:
            try:
                current_commands.append(container.portal_commands)
            except AttributeError:
                break
            try:
                container = container.child_container
            except AttributeError:
                break
        self.current_commands = current_commands

    def set_ui(self):
        """sets the current contexts portal commands"""
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
            'sub_header': '---Front of House Portal---',
            'command_list': 'type: menu, dinning',
            'context': '',
            'footer': '-----------------------------'
        }
        self.child_container: ui_container = None
        self.set_context_dinning()
        print('Front of House Portal: access granted')

    def set_context_menu(self):
        self.foh_data.set_context_menu()
        self.child_container = self.foh_data.get_context().get_ui()

    def set_context_dinning(self):
        self.foh_data.set_context_dinning()
        self.child_container = self.foh_data.get_context().get_ui()


class dinning_room_ui_container(ui_container):
    def __init__(self, dinning_room: 'Dinning_Room'):
        self.dinning_room_data = dinning_room
        self.tables = self.dinning_room_data.get_all_tables_basic()
        self.portal_commands = {}
        for table in self.tables:
            if table[1] is True:
                self.portal_commands[table[0]] = self.dinning_room_data.get_tables()[table[0]]
        self.ui_template = \
            {'header': '-----Select Table Number-----',
             'contex': self.tables}

class menu_ui_container(ui_container):
    def __init__(self, menu: 'Menu'):
        self.menu_data = menu
