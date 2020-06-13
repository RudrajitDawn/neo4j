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



1. __Register Services and APIs :__ ```/registerAll```  
   - request type: POST  
   - example content: <pre>{"TRMservice":["API1","API2","API3"],
                          "CPCservice":["API1","API2","API3"],
                          "XORservice":["API1","API2","API3"]}</pre>  
   - example output: <pre>[
                          "TRMservice created.",
                          "API1 created under TRMservice.",
                          "API2 created under TRMservice.",
                          "API3 created under TRMservice.",
                          "CPCservice created.",
                          "API1 created under CPCservice.",
                          "API2 created under CPCservice.",
                          "API3 created under CPCservice.",
                          "XORservice created.",
                          "API1 created under XORservice.",
                          "API2 created under XORservice.",
                          "API3 created under XORservice."
                    ]</pre>


2. __Create relations :__ ```/createRelation```  
   - request type: POST  
   - example content:
      ```
      {"TRMservice":
         {"API1":
            {"CPCservice":
               {"API2":2},
            "XORservice":
               {"API3":3}
            }
         },
      "CPCservice":
         {"API2":
            {"TRMservice":
               {"API2":1},
            "XORservice":
               {"API1":2}
            }
         },
      "XORservice":
         {"API1":
            {"TRMservice":
               {"API3":3},
            "CPCservice":
               {"API3":1}
            }
         }
      }
      ```
   - example output: <pre>
   [
    "DEPENDENCY created from TRMservice API1 to CPCservice API2 with call_rate 2.",
    "DEPENDENCY created from TRMservice API1 to XORservice API3 with call_rate 3.",
    "DEPENDENCY created from CPCservice API2 to TRMservice API2 with call_rate 1.",
    "DEPENDENCY created from CPCservice API2 to XORservice API1 with call_rate 2.",
    "DEPENDENCY created from XORservice API1 to TRMservice API3 with call_rate 3.",
    "DEPENDENCY created from XORservice API1 to CPCservice API3 with call_rate 1."
]
</pre>

3. __Compute instances of affected APIs :__ ```/computeInstances```  
   - request type: POST  
   - example content:
      ```
      {"TRMservice":
         {"API1":10000},
      "CPCservice":
         {"API2":5000}
      }
      ```
   -example output:
      ```
      [{
              "messages": []
          },
          {
              "CPCservice": {
                  "API1": 0,
                  "API2": 25000,
                  "API3": 50000
              },
              "TRMservice": {
                  "API1": 10000,
                  "API2": 25000,
                  "API3": 150000
              },
              "XORservice": {
                  "API1": 50000,
                  "API2": 0,
                  "API3": 30000
              }
          }
      ]
      ```
