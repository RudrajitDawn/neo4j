# neo4j
#### Maintain an acyclic directed graph using Flask (for REST api) and neo4j (for GRAPH DATABASE) in python

Enter into the folder neo4j-1.7.6 . Here is a python script "main.py" .

In "main.py" enter authentication details to the database like 
```
driver = GraphDatabase.driver('bolt://34.224.83.145:34364', auth=basic_auth('neo4j', 'differences-tests-man'))
```
One can create a blank sandbox in https://sandbox.neo4j.com/ and can work there.

The basic model of the graph is 

![data_model](https://github.com/RudrajitDawn/neo4j/blob/master/data_model.png)

One can use the apis for create, read, compute, update like this:

Create a service : ```/createService/<service_name>```  
Create an API : ```/<service_name>/createApi/<api_name>```  
Create a relation : ```/createRelation/<service_name1>/<api_name1>/<relation_type>/<service_name2>/<api_name2>/<attribute>/<int:weight>```  
Compute instances of all APIs : ```/computeInstances```  
Update a relation : ```/updateRelation/<service_name1>/<api_name1>/<relation_type>/<service_name2>/<api_name2>/<attribute>/<int:weight>```  
Read number of instances of all APIs : ```/readInstances```  
