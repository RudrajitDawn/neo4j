#compute number of required instances of each api for first time

def compute_instances(session):
	
	cypher_query = 'match (:API)-[r:REQUEST]->(a1:API) set a1.no_of_required_instances=a1.no_of_required_instances+r.request_rate with r.request_rate as downstream,a1 '
	
	for i in range(1,100):
		cypher_query += 'match (a{f})-[d:DEPENDENCY]->(a{l}:API) set a{l}.no_of_required_instances=a{l}.no_of_required_instances+downstream*d.call_rate with downstream*d.call_rate as downstream,a{l} '.format(f = str(i), l = str(i+1))
	
	session.run(cypher_query[:-47], parameters={})
	
	return 'DONE'
	
