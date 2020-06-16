#read number of required instances of all apis

def read_all_instances(session):
	
	cypher_query = 'match (s:SERVICE)-[:HAS]->(a:API) return s.name as service_name, a.name as api_name, a.no_of_required_instances as no_of_required_instances'
	results = session.run(cypher_query, parameters={})
	
	result = []
	
	def find_service_name(result, service_name):
		for i in range(len(result)):
			if result[i]['service_name'] == service_name:
				return i
		return -1
	
	for record in results:
		service_name = record['service_name']
		api_name = record['api_name']
		instances = record['no_of_required_instances']
		sindex = find_service_name(result, service_name)
		if sindex == -1:
			result.append({'service_name':service_name, 'api_names':{}})
			sindex = len(result)-1
		result[sindex]['api_names'][api_name] = instances
	
	return result
	
