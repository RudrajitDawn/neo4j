from neo4j import GraphDatabase, basic_auth

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

driver = GraphDatabase.driver('bolt://localhost:7687', auth = basic_auth('neo4j', 'abcxyz'), encrypted = False)
session = driver.session()

import create

class register_services_and_apis(Resource):
	def post(self):
		details = request.json
		results = []
		for service_name in details.keys():
			results.append(create.create_service(session, service_name))
			for api_name in details[service_name]:
				results.append(create.create_api(session, service_name, api_name))
		return jsonify(results)

class create_relation(Resource):
	def post(self):
		relations = request.json
		results = []
		for service_name1 in relations.keys():
			for api_name1 in relations[service_name1].keys():
				for service_name2 in relations[service_name1][api_name1].keys():
					for api_name2 in relations[service_name1][api_name1][service_name2].keys():
						results.append(create.create_relation(session, service_name1, api_name1, "DEPENDENCY", service_name2, api_name2, "call_rate", relations[service_name1][api_name1][service_name2][api_name2]))
		return jsonify(results)

import compute

class compute_instances(Resource):
	def post(self):
		starting_positions = request.json
		return jsonify(compute.distribute_multiple_weights(session,starting_positions))

'''import update

class update_relation(Resource):
	def get(self, service_name1, api_name1, relation_type, service_name2, api_name2, attribute, weight):
		return jsonify('Changed things are: ',update.update_relation(session, service_name1, api_name1, relation_type, service_name2, api_name2, attribute, weight))

import read

class read_all_instances(Resource):
	def get(self):
		return jsonify(read.read_all_instances(session))'''

class Home(Resource):
	def get(self):
		return 'WELCOME'

api.add_resource(Home,'/')
api.add_resource(register_services_and_apis,'/registerAll')
api.add_resource(create_relation,'/createRelation')
api.add_resource(compute_instances,'/computeInstances')
#api.add_resource(update_relation,'/updateRelation/<service_name1>/<api_name1>/<relation_type>/<service_name2>/<api_name2>/<attribute>/<int:weight>')
#api.add_resource(read_all_instances,'/readInstances')
app.run(debug=True)

