#read number of required instances of all apis

def read_all_instances(session):
	
	cypher_query = 'match (s:SERVICE)-[:HAS]->(a:API) return s.name as service_name, a.name as api_name, a.no_of_required_instances as no_of_required_instances'
	results = session.run(cypher_query, parameters={})
	
	result = {}
	
	for record in results:
		service_name = record['service_name']
		api_name = record['api_name']
		instances = record['no_of_required_instances']
		if service_name not in result.keys():
			result[service_name] = {}
		result[service_name][api_name] = instances
	
	return result
	
