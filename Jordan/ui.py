from Jordan.login_portal import LoginPortal
from functools import partial

class portal_ui_container:
    """Using MVC pattern:
    https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller"""
    from portal import MainPortal
    def __init__(self, portal_data:MainPortal):
        self.portal_data = portal_data
        self.child_container = portal_data._p
        self.portal_commands = \
            {'help': partial(self.print_help, self.portal_commands),
            'login': self.portal_data.login,
            'exit': exit()}
        self.ui_template = \
            {'header': 'Kozy Koala App',
            'context': self.context.ui_template,
            'footer': '-----------------------------'}
        print(self.ui_template)

    def print_help(self, portal_commands):
        print(self.ui_template['header'])
        for key in portal_commands.keys():
            print(key)
        print(self.ui_template['footer'])

    def user_in(self):
        return input("type help for commands")


class foh_ui_container:

    def __init__(self):
        self.ui_template = {'sub_header': 'Front of House Portal',
                            'context': 'Front of House Portal: access granted',
                            'footer': '-----------------------------'}

    def set_description(self):

    def set_sub_section(self, context):
        self.ui_template['context'] = context



