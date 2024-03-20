import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import check_authentication, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, create_collection

class ActionReset(Resource):
    def __init__(self, **kwargs):
        logging.info('ActionReset init called')
        self.root = PATHS['Root']
        self.auth = kwargs['auth']

    def post(self, ManagerId):
        logging.info('ActionReset post called')
        msg, code = check_authentication(self.auth)

        if code == 200:
            logging.info('The emulator has been restarted.')
            return 'ok', 200
            #Reset.do_reset()
        else:
            return msg, code
