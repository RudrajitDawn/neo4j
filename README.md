# neo4j
#### Maintain an acyclic directed graph using Flask (for REST api) and neo4j (for GRAPH DATABASE) in python

Enter into the folder neo4j-1.7.6 . Here is a python script "main.py" .

In "main.py" enter authentication details to the database like 
```
driver = GraphDatabase.driver('bolt://localhost:7687', auth = basic_auth('neo4j', 'abcxyz'), encrypted = False)
```
One can create a blank sandbox in https://sandbox.neo4j.com/ and can work there or can download neo4j desktop.

The basic model of the graph is 

![data_model](https://github.com/RudrajitDawn/neo4j/blob/master/data_model.png)
\
\
One can use the apis for create, read, compute, update like this:



1. __Create a service :__ ```/createService```  
   - request type: POST  
   - example content: <pre><code>["TRMservice","CPCservice","XORservice"]</code></pre>



2. __Create an API :__ ```/createApi```  
   - request type: POST  
   - example content: <pre><code>{"TRMservice":["API1","API2","API3"],
                          "CPCservice":["API1","API2","API3"],
                          "XORservice":["API1","API2","API3"]}</code></pre>  



3. __Create a relation :__ ```/createRelation```  
   - request type: POST  
   - example content: <pre></code>{"TRMservice API1":
                                 {"CPCservice API2":2,"XORservice API3":3},
                          "CPCservice API2":
                                 {"TRMservice API2":1,"XORservice API1":2},
                          "XORservice API1":
                                 {"TRMservice API3":3,"CPCservice API3":1}
                         }</code></pre>



4. __Compute instances of affected APIs :__ ```/computeInstances```  
   - request type: POST  
   - example content:  <pre><code>{"TRMservice API1":10000,"CPCservice API2":5000}</code></pre>



5. __Read number of instances of all APIs :__ ```/readInstances```  
   - request type: GET  
