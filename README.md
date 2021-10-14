# Discount generator through microservices

Overview
=========

The idea of this project is to develop a solution using microservices structure to generate discount codes for brands which will be provided to users when requested. Obviously there are lot of limitations here, lot could be improved. But should be enough to give an idea how microservices work :)

Requirements
=============

* Python 3.x
* Local version of AWS DynamoDB available in your machine and running over port 8000 (Check [this document in AWS](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) if you don't have the local version already)


Installation & Running
=======================
* Download the codebase and go to the root directory
* Make sure DynamoDB is running over default port (8000) in your machine
* Run <code>$ make install</code> to initialize python virtualenv, installing requirements and setting up the tables.
_This will also create a sample user in the database with user_id and user_secret which you will need to test the discount provider service._
* Run <code>$ make launch</code> to start the services. There are two services: Discount Generator running in port 5001 and Discount Provider running in port 5002.
* If you want to stop the services, run <code>$ make shutdown</code>


API Endpoints
==============

## Generating X number of discounts for a brand.


### Request

`POST /discounts/api/v1.0/generate`

    curl -i -H 'Content-Type: application/json' -d '{"brand_id": 1,"number_of_codes": 100}' http://127.0.0.1:5001/discounts/api/v1.0/generate

### Response

	HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 121
	Server: Werkzeug/2.0.2 Python/3.8.3
	Date: Thu, 14 Oct 2021 13:00:51 GMT

	{
	  "code": "201", 
	  "data": "", 
	  "message": "System generated discount codes successfully", 
	  "status": "success"
	}

## Get a discount for a user from Brand X

### Request

`GET /discounts/api/v1.0/get_code/user_id/user_secret/brand_id`

    curl -i -H 'Content-Type: application/json' http://127.0.0.1:5002/discounts/api/v1.0/get_code/2341/jhjdvbfehfbu468hGFVYUGHBIUIUYRD/2

### Response

	HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 85
	Server: Werkzeug/2.0.2 Python/3.8.3
	Date: Thu, 14 Oct 2021 13:03:41 GMT

	{
	  "code": "201", 
	  "data": "7U7I845L", 
	  "message": "", 
	  "status": "success"
	}



-------------- The Force Awakens -----------