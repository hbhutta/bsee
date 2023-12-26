# AWS
AWS EC2 gives virtual machine 
AWS 

# Products geared for web apps:
AWS labmda is a serverless compute service that lets us run code without provisiining or managing servers
- upload code to aws and aws handles the rest
- - When an event tha causes code to run happens, we pull servers from the reserve pool and it will deploy the lambda function onto the server so they can run the code

lambda use cases
- File processing 
- Stream procesisng
- web apps
- mobile/web backends
- API can be built with lambda functions and API gateway ***

lambda function is just the code you want to run

Trigger determines when code runs 
We have to tell AWS when we want our code to run
e.g. trigger code whenver there is a request to an API gateway
e.g. trigger code wherenver there is update to dynamo db
e.g. "" "" when upload file to s3

Event is information about trigger


Serverless is not actually serverless because of reserve pools which contains servers that are used on a need basis and then returned to the pool


ex. Converting a simple Python function into an AWS lambda function
def foo (l, w): return l * w [Calculate area]
--> def foo(event: json, context) return data = l * w; json.dumps(data)


Different API types for API gateway: 
1. HTTP API
2. REST API (this is what we have)
3. Websocket API



