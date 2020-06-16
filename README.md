# neo4j
#### Maintain an acyclic directed graph using Flask (for REST api) and neo4j (for GRAPH DATABASE) in python

One can download neo4j desktop from https://neo4j.com/download/neo4j-desktop/?edition=desktop&flavour=unix&release=1.2.9&offline=true .

Some dependencies are here like flask(for REST api), neo4j(for graph database). One can install them via pip.
```
pip3 install flask-restful
pip3 install neo4j
```
The basic model of the graph is 

![data_model](https://github.com/RudrajitDawn/neo4j/blob/master/data_model.png)
\
\
Enter into the folder project . Here is a python script "main.py" .

In "main.py" enter authentication details to the database like 
```
driver = GraphDatabase.driver('bolt://localhost:7687', auth = basic_auth('neo4j', 'abcxyz'), encrypted = False)
```
Next for using the apis some rest api platform is required. One option is:  
Open https://reqbin.com/ . Add extension if required. One can give inputs and get outputs in JSON format very easily here.
\
\
Next run in a terminal from project directory: ```python3 main.py```
\
Some initiation steps one can see in terminal. One will get the server address and port there. By default it is:
http://127.0.0.1:5000/  
This is the base url. Final urls will be like:  
http://127.0.0.1:5000/registerAll  
http://127.0.0.1:5000/createRelation  
\
\
One can use the apis for create, read, compute like this:  

1. __Register Services and APIs :__ ```/registerAll```  
   - request type: POST  
   - example content: <pre>{"registration":
	   [{"service_name":"CPCservice","api_names":["API1","API2","API3"]},
	   {"service_name":"TRMservice","api_names":["API1","API2","API3","API4"]},
	   {"service_name":"XORservice","api_names":["API1","API2","API3"]}]
	   }
      </pre>  
   - example output: <pre>[
                         "CPCservice created.",
                         "API1 created under CPCservice.",
                         "API2 created under CPCservice.",
                         "API3 created under CPCservice.",
                         "TRMservice created.",
                         "API1 created under TRMservice.",
                         "API2 created under TRMservice.",
                         "API3 created under TRMservice.",
                         "API4 created under TRMservice.",
                         "XORservice created.",
                         "API1 created under XORservice.",
                         "API2 created under XORservice.",
                         "API3 created under XORservice."
                     ]</pre>


2. __Create relations :__ ```/createRelation```  
   - request type: POST  
   - example content:
      ```
      {"relations":
         [{"service_name":"TRMservice","api_names":
            {"API1":
               {"DEPENDENCY":
                  [{"service_name":"CPCservice","api_names":
                     {"API2":{"call_rate":2}}
                  },
                  {"service_name":"XORservice","api_names":
                     {"API3":{"call_rate":3}}
                  }]
               }
            }
         },
         {"service_name":"CPCservice","api_names":
            {"API2":
               {"DEPENDENCY":
                  [{"service_name":"TRMservice","api_names":
                     {"API2":{"call_rate":1},
                     "API4":{"call_rate":2}}
                  },
                  {"service_name":"XORservice","api_names":
                     {"API1":{"call_rate":2}}
                  }]
               }
            }
         },
         {"service_name":"XORservice","api_names":
            {"API1":
               {"DEPENDENCY":
                  [{"service_name":"TRMservice","api_names":
                     {"API3":{"call_rate":3}}
                  },
                  {"service_name":"CPCservice","api_names":
                     {"API3":{"call_rate":1}}
                  }]
               }
            }
         }]
      }
      ```
   - example output: <pre>
   [
    "DEPENDENCY created from TRMservice API1 to CPCservice API2 with call_rate 2.",
    "DEPENDENCY created from TRMservice API1 to XORservice API3 with call_rate 3.",
    "DEPENDENCY created from CPCservice API2 to TRMservice API2 with call_rate 1.",
    "DEPENDENCY created from CPCservice API2 to TRMservice API4 with call_rate 2.",
    "DEPENDENCY created from CPCservice API2 to XORservice API1 with call_rate 2.",
    "DEPENDENCY created from XORservice API1 to TRMservice API3 with call_rate 3.",
    "DEPENDENCY created from XORservice API1 to CPCservice API3 with call_rate 1."
   ]
   </pre>

3. __Compute instances of affected APIs :__ ```/computeInstances```  
   - request type: POST  
   - example content:
      ```
      {"compute":
         [{"service_name":"TRMservice","api_names":
            {"API1":{"hit_rate":10000}}
         },
          {"service_name":"CPCservice","api_names":
            {"API2":{"hit_rate":5000}}
         }],
	 "depth":100
      }
      ```
   - example output:
      ```
      {
          "instance_details": [{
                  "api_names": {
                      "API1": 0,
                      "API2": 25000,
                      "API3": 50000
                  },
                  "service_name": "CPCservice"
              },
              {
                  "api_names": {
                      "API1": 10000,
                      "API2": 25000,
                      "API3": 150000,
                      "API4": 50000
                  },
                  "service_name": "TRMservice"
              },
              {
                  "api_names": {
                      "API1": 50000,
                      "API2": 0,
                      "API3": 30000
                  },
                  "service_name": "XORservice"
              }
          ],
          "messages": []
      }
      ```
For computing the required instances, one can set the depth value inside the input json. It actually decides how far to follow relations from starting nodes. For example if depth value is 0, then only the required instances of starting nodes will be changed. No relation will be followed. If the depth value is 1, then the nodes directly attached to starting nodes will be updated. Just test with two or three examples to understand properly. To follow entire path, one can give some large value like 100 (not too large).  
\
One can use these methods any number of time. Like one can create new services and apis and relations after first time using the same methods.  
\
If some message comes like "Request timeout." after doing everything correct, one can just restart the server(means terminate the program in terminal and again run ```python3 main.py```). It can also happen for giving large value of depth.  
