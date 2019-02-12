# geometric_state_service
REST services to determine the state name by giving the coordinate of the point (longitude, altitude)

#Problem and Requirements:
## State Server!
Part One: Please create a server and an endpoint that will serve geometries that are included in states.json file.

Part Two: Next is a service that will consume that endpoint and tell us which state, if any, a point is in.


Some simplified geometries are included in states.json (so greatly simplified,
that some of the smaller ones disappear).

### Expected Behavior
$ ./state-server &

$ ./endpoint-server &

$ curl  -d "longitude=-77.036133&latitude=40.513799" http://localhost:8080/
  
["Pennsylvania"]

$

#Solution and Design considerations:
##Design considerations:
#### Why do we need separate the state-server and the endpoint-server?
    From business perspective, it might not be necessary to separate these two functions (1. read states.json to create the geometries for states, 2.finding the state of a giving point) into two different process. Function No.2 is really tightly coupled with Function No.1. It is also not very efficient to pass the json/dictionary object crossing two different processes.
    But it is a good design if we are thinking to scale different services for different level of scalability requirements. In this case, the states geometris (state-server) can be cached in somewhere (ElasticCache, Reddis or NoSQL stores..etc). The endpoint-server can scale horizontally to meet the different level of scalability requirements.

#### How do the endpoint-server communicate with state-server?
    This really depends on how we want scale the system. For example, if we use cache to cache the states geometries, the state-server can just put the states geometries into cache and make sure it is up to date. The endpoint-server can only read the states geometries from the shared cache. Also the state-server can use some kind of event notification mechanism to notify the endpoint-server when there is changes to the states geometries(if there has changes, for this case, it most likely are relatively static).
    It can also use RPC to communicate each other if there is no need to expose the state-server service to other clients' access and the communication efficiency is a big concern between state-server and endpoint-server.
    If both services are required to expose to other clients access and would like to scale better in cloud environment, the RESTful services should be better solution (Implemented)

#### How to implement the RESTful services for these two servers?
    BaseHTTPServer is a simple solution for PoC and small scale of system. (Implemented)
    Flask a lightweight python RESTful framework can be used for enterprise production level system for the speed concerns and NoSQL support which is very good fit for microservices system (will try if have time)
    Django RESTFul framework can take advantages of the features of Django itself. It is good for large scale of REST services which require versioning support and ORM.(may just create skeleton for future extension if have time)

# Running instructions:
 Requirements:  Python3
### Steps:
1. git clone https://github.com/rongyj/geometry_state_services.git
2. cd geometry_state_services
3. make
4. ./state-server &
5. ./endpoint-server &
6. curl  -d "longitude=-77.036133&latitude=40.513799" http://localhost:8080/

You have to manually kill the two python processes after the test.