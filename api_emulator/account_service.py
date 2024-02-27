# Copyright Notice:
# Copyright 2016-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/main/LICENSE.md

# Redfish Emulator Role Service.
#   Temporary version, to be removed when AccountService goes dynamic

class AccountService(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AccountService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_accounts'):
            self._accounts = {
                'Administrator': 'Password',
            }
            self._roles = {
                'Administrator': 'Administrator',
            }
    def checkPriviledgeLevel(self, user, level):
        if self._roles[user] == level:
            return True
        else:
            return False

    def getPassword(self, username):
        if username in self._accounts:
            return self._accounts[username]
        else:
            return None

    def addUser(self, username, password, role):
        if username in self._accounts:
            return None
        else:
            self._accounts[username] = password
            self._roles[username] = role

    def checkPrivilege(self, privilege, username, errorResponse):
        def wrap(func):
            def inner(*args, **kwargs):
                if self.checkPriviledgeLevel(username(), privilege):
                    return func(*args, **kwargs)
                else:
                    return errorResponse()
            return inner
        return wrap
