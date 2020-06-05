#read number of required instances of all apis

def read_all_instances(session):
	
	cypher_query = 'match (s:SERVICE)-[:HAS]->(a:API) return s.name+" "+a.name+" "+a.no_of_required_instances as details'
	results = session.run(cypher_query, parameters={})
	
	result = []
	
	for record in results:
		result.append(record['details'])
	
	return result
	
