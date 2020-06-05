from neo4j import GraphDatabase, basic_auth

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

driver = GraphDatabase.driver('bolt://34.224.83.145:34364', auth=basic_auth('neo4j', 'differences-tests-man'))
session = driver.session()

import create

class create_service(Resource):
	def get(self, service_name):
		return jsonify(create.create_service(session, service_name))

class create_api(Resource):
	def get(self, service_name, api_name):
		return jsonify(create.create_api(session, service_name, api_name))

class create_relation(Resource):
	def get(self, service_name1, api_name1, relation_type, service_name2, api_name2, attribute, weight):
		return jsonify(create.create_relation(session, service_name1, api_name1, relation_type, service_name2, api_name2, attribute, weight))

import compute

class compute_instances(Resource):
	def get(self):
		return jsonify(compute.compute_instances(session))

import update

class update_relation(Resource):
	def get(self, service_name1, api_name1, relation_type, service_name2, api_name2, attribute, weight):
		return jsonify('Changed things are: ',update.update_relation(session, service_name1, api_name1, relation_type, service_name2, api_name2, attribute, weight))

import read

class read_all_instances(Resource):
	def get(self):
		return jsonify(read.read_all_instances(session))

class Home(Resource):
	def get(self):
		return 'WELCOME'

api.add_resource(Home,'/')
api.add_resource(create_service,'/createService/<service_name>')
api.add_resource(create_api,'/<service_name>/createApi/<api_name>')
api.add_resource(create_relation,'/createRelation/<service_name1>/<api_name1>/<relation_type>/<service_name2>/<api_name2>/<attribute>/<int:weight>')
api.add_resource(compute_instances,'/computeInstances')
api.add_resource(update_relation,'/updateRelation/<service_name1>/<api_name1>/<relation_type>/<service_name2>/<api_name2>/<attribute>/<int:weight>')
api.add_resource(read_all_instances,'/readInstances')
app.run(debug=True)

