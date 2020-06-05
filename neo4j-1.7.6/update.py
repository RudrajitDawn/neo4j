def get_value(results,attribute):
	for r in results:
		return r[attribute]

def service_is_present(session, service_name):
	
	cypher_query = 'match (s:SERVICE{name:{sname}}) return count(s) as count'
	results = session.run(cypher_query, parameters={'sname':service_name})
	
	return get_value(results, 'count') != 0

def api_is_present(session, service_name, api_name):
	
	cypher_query = 'match (:SERVICE{name:{sname}})-[:HAS]->(:API{name:{aname}}) return count(*) as count'
	results = session.run(cypher_query, parameters={'sname':service_name, 'aname':api_name})
	
	return get_value(results, 'count') != 0

def present_relation_value(session, service_name1, api_name1, relation_type, service_name2, api_name2, attribute):
	
	cypher_query = 'match (:SERVICE{name:{sname1}})-[:HAS]->(:API{name:{aname1}})-[r:_rt_]->(:API{name:{aname2}})<-[:HAS]-(:SERVICE{name:{sname2}}) return r._attr_ as weight'
	
	cypher_query = cypher_query.replace('_rt_', relation_type)
	cypher_query = cypher_query.replace('_attr_', attribute)
	
	results = session.run(cypher_query, parameters={'sname1':service_name1, 'aname1':api_name1, 'sname2':service_name2, 'aname2':api_name2})
	
	return get_value(results, 'weight')

#update a relation

def update_relation(session, service_name1, api_name1, relation_type, service_name2, api_name2, attribute, weight):
	
	#check services and apis participating in relation are present or not
	
	if not service_is_present(session, service_name1):
		return service_name1+' does not exist.'
	if not api_is_present(session, service_name1, api_name1):
		return api_name1+' is not present under '+service_name1+'.'
	if not service_is_present(session, service_name2):
		return service_name2+' does not exist.'
	if not api_is_present(session, service_name2, api_name2):
		return api_name2+' is not present under '+service_name2+'.'
	present_weight = present_relation_value(session, service_name1, api_name1, relation_type, service_name2, api_name2, attribute)
	
	#store present weight before modifying it
	
	if present_weight == None:
		cypher_query = 'match (:SERVICE{name:{sname1}})-[:HAS]->(a0:API{name:{aname1}}), (:SERVICE{name:{sname2}})-[:HAS]->(a1:API{name:{aname2}}) create (a0)-[r:_rt_{_attr_:{w}}]->(a1) '
	
		cypher_query = cypher_query.replace('_rt_', relation_type)
		cypher_query = cypher_query.replace('_attr_', attribute)
		
		present_weight = 0
		
	else:
		cypher_query = 'match (:SERVICE{name:{sname1}})-[:HAS]->(a0:API{name:{aname1}})-[r:_rt_]->(a1:API{name:{aname2}})<-[:HAS]-(:SERVICE{name:{sname2}}) set r._attr_={w} '
		
		cypher_query = cypher_query.replace('_rt_', relation_type)
		cypher_query = cypher_query.replace('_attr_', attribute)
	
	#change the no_of_required_instances following the graph
	
	if relation_type == 'REQUEST' and attribute == 'request_rate':
		cypher_query += 'set a1.no_of_required_instances=a1.no_of_required_instances+{w}-{pw},a1.changed=1 with {w}-{pw} as downstream,a1 '
	
	if relation_type == 'DEPENDENCY' and attribute == 'call_rate':
		cypher_query += 'set a1.no_of_required_instances=a1.no_of_required_instances+({w}-{pw})*a0.no_of_required_instances,a1.changed=1 with ({w}-{pw})*a0.no_of_required_instances as downstream,a1 '
	
	for i in range(1,100):
		cypher_query += 'match (a{f})-[d:DEPENDENCY]->(a{l}:API) set a{l}.no_of_required_instances=a{l}.no_of_required_instances+downstream*d.call_rate,a{l}.changed=1 with downstream*d.call_rate as downstream,a{l} '.format(f = str(i), l = str(i+1))
	
	session.run(cypher_query[:-47], parameters={'sname1':service_name1, 'aname1':api_name1, 'sname2':service_name2, 'aname2':api_name2, 'w':weight, 'pw':present_weight})
	
	#give only changed values output
	
	cypher_query='match(s:SERVICE)-[:HAS]->(a:API) where not a.changed is null remove a.changed return s.name+" "+a.name+" "+a.no_of_required_instances as changed_api'
	
	results = session.run(cypher_query, parameter={})
	
	result = []
	
	for record in results:
		result.append(record['changed_api'])
	
	return result
	
