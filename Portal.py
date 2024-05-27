# import time
#
# from Inherit_Module import ITokenGuide
# # from Login import LoginPortal, User_Token, TKeys
# from threading import Event
#
#
# class Portal(ITokenGuide):
#     """Main Portal, _portal is the current context"""
#
#     def __init__(self, exit_func):
#
#         self._exit = exit_func  # sessions exit function
#         self._token = None
#         self._portal = None
#
#         _help = " "
#         portal_commands = {'help': print(_help), 'login': self.Login(), 'exit': self._exit()}
#         _help = portal_commands
#
#         self.Login()
#         while True:
#             user_in = input("type help for commands")
#
#             if user_in in portal_commands:
#                 portal_commands.get(user_in)
#             else:
#                 print('invalid input')
#
#     from Login import LoginPortal, User_Token, TKeys
#     def PossesToken(self, user: User_Token):
#         self._token = user
#
#     def GuideToken(self, next_guide: ITokenGuide):
#         next_guide.GuideToken(self._token)
#
#     def AccessLevel(self) -> int:
#         return 0
#
#     def Login(self):
#         from Login import LoginPortal, User_Token, TKeys
#         """Logs in user and instantiates portal once it is finished processing
#                via ACL inside Login"""
#         self._portal = LoginPortal(self)
#         if self._portal.Login():
#             # thread safety
#             while self._token is None:
#                 time.sleep(0.1)
#             self._token: User_Token
#             # instantiates main Portal context
#             self._portal = self._token.data[TKeys.PortalKey]()
#             print("Login Successful")
#
#
# class FOHPortal:
#
#     def __init__(self):
#         print("Front of House Portal Access")
#
#
# class BOHPortal:
#
#     def __init__(self):
#         print("Back of House Portal Access")
#
#
# class BusinessPortal:
#
#     def __init__(self):
#         print("Business Portal Access")
