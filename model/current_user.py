# class CurrentUser:
#     _instance = None

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super(CurrentUser, cls).__new__(cls, *args, **kwargs)
#             cls._instance._initialize()
#         return cls._instance

#     def _initialize(self):
#         self.user_details = {
#             'id_number': '',
#             'firstname': '',
#             'lastname': '',
#             'othernames': '',
#             'user_type': ''
#             # Add other fields as necessary
#         }

#     def set_user_details(self, id_number, firstname, lastname,othernames, user_type):
#         self.user_details['id_number'] = id_number
#         self.user_details['firstname'] = firstname
#         self.user_details['lastname'] = lastname
#         self.user_details['othernames'] = othernames
#         self.user_details['user_type'] = user_type

#     def get_user_details(self):
#         return self.user_details

#     def logout(self):
#         # Clear user details
#         self._initialize()
