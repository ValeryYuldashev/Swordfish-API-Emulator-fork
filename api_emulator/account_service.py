# Copyright Notice:
# Copyright 2016-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/main/LICENSE.md

# Redfish Emulator Role Service.
#   Temporary version, to be removed when AccountService goes dynamic

class AccountService(object):

    def __init__(self):
        self._accounts = { 'Dmitry': '1',
                           'Valery': '2',
                           'Ivan': '3' }
        self._roles = { 'Dmitry': 'DevOps',
                        'Valery': 'Administrator',
                        'Ivan': 'StorageAdmin' }

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
            return False
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
