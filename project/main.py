from neo4j import GraphDatabase, basic_auth

from flask import Flask, jsonify, request
from flask_restplus import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

driver = GraphDatabase.driver('bolt://localhost:7687', auth = basic_auth('neo4j', 'abcxyz'), encrypted = False)
session = driver.session()

import create

class register_services_and_apis(Resource):
	def post(self):
		details = request.json
		results = []
		for record in details['registration']:
			service_name = record['service_name']
			results.append(create.create_service(session, service_name))
			for api_name in record['api_names']:
				results.append(create.create_api(session, service_name, api_name))
		return jsonify(results)

class create_relation(Resource):
	def post(self):
		relations = request.json['relations']
		results = []
		for node1 in relations:
			service_name1 = node1['service_name']
			for api_name1 in node1['api_names'].keys():
				for rel_type in node1['api_names'][api_name1].keys():
					for node2 in node1['api_names'][api_name1][rel_type]:
						service_name2 = node2['service_name']
						for api_name2 in node2['api_names'].keys():
							for attr in node2['api_names'][api_name2].keys():
								results.append(create.create_relation(session, service_name1, api_name1, rel_type, service_name2, api_name2, attr, node2['api_names'][api_name2][attr]))
		return jsonify(results)

import compute

class compute_instances(Resource):
	def post(self):
		starting_positions, depth = request.json['compute'], request.json['depth'] + 1
		return jsonify(compute.distribute_multiple_weights(session, starting_positions, depth))

class Home(Resource):
	def get(self):
		return 'WELCOME'

api.add_resource(Home,'/')
api.add_resource(register_services_and_apis,'/registerAll')
api.add_resource(create_relation,'/createRelation')
api.add_resource(compute_instances,'/computeInstances')
app.run(debug=True)

