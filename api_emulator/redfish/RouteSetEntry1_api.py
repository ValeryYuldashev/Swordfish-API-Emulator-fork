#
# Copyright (c) 2017-2021, The Storage Networking Industry Association.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# Neither the name of The Storage Networking Industry Association (SNIA) nor
# the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#  THE POSSIBILITY OF SUCH DAMAGE.

# Resource implementation for - /redfish/v1/Fabrics/{FabricId}/Switches/{SwitchId}/Ports/{PortId}/MPRT/{MPRTId}/RouteSet/{RouteId}
# Program name - RouteSetEntry1_api.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.RouteSetEntry1 import get_RouteSetEntry1_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# RouteSetEntry1 Collection API
class RouteSetEntry1CollectionAPI(Resource):
	def __init__(self):
		logging.info('RouteSetEntry1 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, FabricId, SwitchId, PortId, MPRTId):
		logging.info('RouteSetEntry1 Collection get called')
		path = os.path.join(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet', 'index.json').format(FabricId, SwitchId, PortId, MPRTId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, FabricId, SwitchId, PortId, MPRTId):
		logging.info('RouteSetEntry1 Collection post called')

		if MPRTId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet').format(FabricId, SwitchId, PortId, MPRTId)
		if not os.path.exists(path):
			os.mkdir(path)
			create_collection (path, 'RouteSetEntry')

		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		if request.data:
			config = json.loads(request.data)
			if "@odata.id" in config:
				return RouteSetEntry1API.post(self, os.path.basename(config['@odata.id']))
			else:
				return RouteSetEntry1API.post(self, str(res))
		else:
			return RouteSetEntry1API.post(self, str(res))

	# HTTP PUT Collection
	def put(self, FabricId, SwitchId, PortId, MPRTId):
		logging.info('RouteSetEntry1 Collection put called')

		path = os.path.join(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet', 'index.json').format(FabricId, SwitchId, PortId, MPRTId)
		put_object (path)
		return self.get(FabricId)

# RouteSetEntry1 API
class RouteSetEntry1API(Resource):
	def __init__(self):
		logging.info('RouteSetEntry1 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, FabricId, SwitchId, PortId, MPRTId, RouteId):
		logging.info('RouteSetEntry1 get called')
		path = create_path(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet/{4}', 'index.json').format(FabricId, SwitchId, PortId, MPRTId, RouteId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, FabricId, SwitchId, PortId, MPRTId, RouteId):
		logging.info('RouteSetEntry1 post called')
		path = create_path(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet/{4}').format(FabricId, SwitchId, PortId, MPRTId, RouteId)
		collection_path = os.path.join(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet', 'index.json').format(FabricId, SwitchId, PortId, MPRTId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			RouteSetEntry1CollectionAPI.post(self, FabricId, SwitchId, PortId, MPRTId)

		if RouteId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'FabricId':FabricId, 'SwitchId':SwitchId, 'PortId':PortId, 'MPRTId':MPRTId, 'RouteId':RouteId, 'rb':g.rest_base}
			config=get_RouteSetEntry1_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('RouteSetEntry1API POST exit')
		return resp

	# HTTP PUT
	def put(self, FabricId, SwitchId, PortId, MPRTId, RouteId):
		logging.info('RouteSetEntry1 put called')
		path = os.path.join(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet/{4}', 'index.json').format(FabricId, SwitchId, PortId, MPRTId, RouteId)
		put_object(path)
		return self.get(FabricId, SwitchId, PortId, MPRTId, RouteId)

	# HTTP PATCH
	def patch(self, FabricId, SwitchId, PortId, MPRTId, RouteId):
		logging.info('RouteSetEntry1 patch called')
		path = os.path.join(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet/{4}', 'index.json').format(FabricId, SwitchId, PortId, MPRTId, RouteId)
		patch_object(path)
		return self.get(FabricId, SwitchId, PortId, MPRTId, RouteId)

	# HTTP DELETE
	def delete(self, FabricId, SwitchId, PortId, MPRTId, RouteId):
		logging.info('RouteSetEntry1 delete called')
		path = create_path(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet/{4}').format(FabricId, SwitchId, PortId, MPRTId, RouteId)
		base_path = create_path(self.root, 'Fabrics/{0}/Switches/{1}/Ports/{2}/MPRT/{3}/RouteSet').format(FabricId, SwitchId, PortId, MPRTId)
		return delete_object(path, base_path)

