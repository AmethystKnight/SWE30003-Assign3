from Jordan.login_portal import LoginPortal
from functools import partial
from portal_interfaces import Portal
from abc import ABC
class ui_container(ABC):
    # TODO:Make a parent class for ui_container
    pass
class portal_ui_container(ui_container):
    """Consider using MVC pattern:
    https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller"""
    from portal import MainPortal
    def __init__(self, portal_data:MainPortal):
        self.portal_data:Portal = portal_data
        self.child_container:ui_container = portal_data.get_portal().get_ui()
        self.portal_commands = \
            {'help': partial(self.print_help, self.portal_commands),
            'login': self.portal_data.login,
            'exit': self.portal_data.get_exit()}
        self.ui_template = \
            {'header': 'Kozy Koala App',
            'context': self.child_container.ui_template,
            'footer': '-----------------------------'}
        print(self.ui_template)

    def get_portal_commands(self) -> list:
        """Gets all children of the currently instantiated containers"""
        current_commands = [self.portal_commands]
        container:ui_container = self.child_container
        while True:
            try:
                current_commands.append(container.portal_commands)
            except #does container.portal_commands exist
            try:
                container = container.child_container

            except: # does child container exist
        return current_commands

    def print_help(self, portal_commands):
        print(self.ui_template['header'])
        for key in portal_commands.keys():
            print(key)
        print(self.ui_template['footer'])

    def user_in(self):
        _in = input("type help for commands")
        try:
            self.portal_commands[_in]()
        except KeyError:
            print('invalid input')
            self.user_in()


class foh_ui_container(ui_container):
    from portal import FOHPortal
    def __init__(self,foh_data:FOHPortal):

        self.ui_template = {'sub_header': 'Front of House Portal',
                            'context': 'Front of House Portal: access granted',
                            'footer': '-----------------------------'}
        self.portal_commands = {'menu':foh_data.set_context_dinning(),'dinning':foh_data.set_context_menu()}
        self.child_container:Portal
    def set_description(self):

    def set_sub_section(self, context):
        self.ui_template['context'] = context



