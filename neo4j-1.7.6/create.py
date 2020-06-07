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
	
def present_relation_value(session, service_name1, api_name1, relation_type, service_name2, api_name2, attribute):
	
	cypher_query = 'match (:SERVICE{name:$sname1})-[:HAS]->(:API{name:$aname1})-[r:_rt_]->(:API{name:$aname2})<-[:HAS]-(:SERVICE{name:$sname2}) return r._attr_ as weight'
	
	cypher_query = cypher_query.replace('_rt_', relation_type)
	cypher_query = cypher_query.replace('_attr_', attribute)
	
	results = session.run(cypher_query, parameters={'sname1':service_name1, 'aname1':api_name1, 'sname2':service_name2, 'aname2':api_name2})
	
	return get_value(results, 'weight')

#create a new service

def create_service(session, service_name):
	
	if service_is_present(session, service_name):
		return service_name+' already exists.'
	
	else:
		cypher_query = 'create (s:SERVICE{name:$sname,no_of_apis:0})'
		session.run(cypher_query, parameters={'sname':service_name})
		
		return service_name+' created.'

#create a new api		

def create_api(session, service_name, api_name):
	
	if not service_is_present(session, service_name):	
		return service_name+' does not exist.'
	if api_is_present(session, service_name, api_name):
		return api_name+' already present in '+service_name
	
	cypher_query = 'match (s:SERVICE{name:$sname}) with s create (s)-[:HAS]->(:API{name:$aname,no_of_required_instances:0}) set s.no_of_apis=s.no_of_apis+1'
	session.run(cypher_query, parameters={'sname':service_name, 'aname':api_name})
		
	return api_name+' created under '+service_name+'.'
	
#create a new relation or update a relation

def create_relation(session, service_name1, api_name1, relation_type, service_name2, api_name2, attribute, weight):
	
	#check services and apis participating in relation are present or not
	
	if not service_is_present(session, service_name1):
		return service_name1+' does not exist.'
	if not api_is_present(session, service_name1, api_name1):
		return api_name1+' is not present under '+service_name1+'.'
	if not service_is_present(session, service_name2):
		return service_name2+' does not exist.'
	if not api_is_present(session, service_name2, api_name2):
		return api_name2+' is not present under '+service_name2+'.'
	test_weight = present_relation_value(session, service_name1, api_name1, relation_type, service_name2, api_name2, attribute)
	if test_weight != None:
		cypher_query = 'match (s1:SERVICE{name:$sname1})-[:HAS]->(a1:API{name:$aname1})-[r:_rt_]->(a2:API{name:$aname2})<-[:HAS]-(s2:SERVICE{name:$sname2}) set r._attr_=$w'
	
	else:
		cypher_query = 'match (s1:SERVICE{name:$sname1})-[:HAS]->(a1:API{name:$aname1}) match (s2:SERVICE{name:$sname2})-[:HAS]->(a2:API{name:$aname2}) create (a1)-[:_rt_{_attr_:$w}]->(a2)'
	
	cypher_query = cypher_query.replace('_rt_', relation_type)
	cypher_query = cypher_query.replace('_attr_', attribute)
	
	session.run(cypher_query, parameters={'sname1':service_name1, 'aname1':api_name1, 'sname2':service_name2, 'aname2':api_name2, 'w':weight})
	
	return relation_type+' created from '+service_name1+' '+api_name1+' to '+service_name2+' '+api_name2+' with '+attribute+' '+str(weight)+'.'
	
