def get_value(results,attribute):
	for r in results:
		return r[attribute]

def service_is_present(session, service_name):
	
	cypher_query = 'match (s:SERVICE{name:$sname}) return count(s) as count'
	results = session.run(cypher_query, parameters={'sname':service_name})
	
	return get_value(results, 'count') != 0

def api_is_present(session, service_name, api_name):
	
	cypher_query = 'match (:SERVICE{name:$sname})-[:HAS]->(:API{name:$aname}) return count(*) as count'
	results = session.run(cypher_query, parameters={'sname':service_name, 'aname':api_name})
	
	return get_value(results, 'count') != 0

#distribute weight from present node in the graph following dependencies

def distribute_weight(session, service_name, api_name, weight):
	
	if not service_is_present(session, service_name):
		return service_name+' does not exist.'
	if not api_is_present(session, service_name, api_name):
		return api_name+' is not present under '+service_name+'.'
	
	cypher_query = 'match (:SERVICE{name:$sname})-[:HAS]->(a1:API{name:$aname}) set a1.no_of_required_instances=a1.no_of_required_instances+$w with $w as downstream,a1 '
	
	for i in range(1,100):
		cypher_query += 'match (a{f})-[d:DEPENDENCY]->(a{l}:API) set a{l}.no_of_required_instances=a{l}.no_of_required_instances+downstream*d.call_rate with downstream*d.call_rate as downstream,a{l} '.format(f = str(i), l = str(i+1))
	
	session.run(cypher_query[:-47], parameters={'sname':service_name,'aname':api_name,'w':weight})
	
#distribute weights from multiple nodes

import read

def distribute_multiple_weights(session, starting_nodes):
	
	cypher_query = 'match (a:API) set a.no_of_required_instances=0'
	session.run(cypher_query, parameter = {})
	
	results = {'messages':[]}
	
	for starting_node in starting_nodes:
		service_name = starting_node['service_name']
		for api_name in starting_node['api_names']:
			hit_rate = starting_node['api_names'][api_name]['hit_rate']
			message = distribute_weight(session, service_name, api_name, hit_rate)
			if message != None:
				results['messages'].append(message)
	
	results['instance_details'] = (read.read_all_instances(session))
	
	cypher_query = 'match (a:API) remove a.no_of_required_instances'
	session.run(cypher_query, parameter = {})
	
	return results
	
