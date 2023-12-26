# bsee
A RESTful API to get places to visit in the province of British Columbia, Canada!
For indecisive people (like me) who can't figure out where to go over the holidays.

## Description
- Connects to a PostgreSQL database with data on places of BC gathered using ChatGPT prompts and the Google Maps API
- The front-end interacts with an API through two end-points:
  - Getting a random entry from the database (GET)
  - Posting a random entry to the database (POST)
- A simple front-end documents the API endpoints
- Server made with Golang, web-scraper written ins Python
- Get each place in each city in the province, and store as a row in a PostgreSQL database

## Endpoints
- Get a random place to visit in BC

## Tasks
### Web-scraping (ChatGPT prompts, Google Maps API)
1. [X] Enumerate all cities in B.C. in search-compatible form
2. [X] Enumerate each attraction of each city into an Attraction object
3. [X] Connect to PostgreSQL database (using psycopg2) 
4. [X] Automate insertion into database
   1. [ ] Setup environment variable for Google Maps API key in maps.py

### API (Golang, AWS API Gateway, AWS Lambda)
1. Create a function to get a random attraction from the database
   1. [X] Connect to the database
   2. [X] Setup environment variables needed for database connection
   4. [X] Write query statement to get random attraction from database
      1. [ ] Correct city field if incorrect by comparing with address
   5. [ ] Use Google Maps Place Photos API to get the photo of the place randomly picked from the PostgreSQL database (with the intent of sending everything back to the front-end) -- but first get the API going on AWS with just the (name, city, address) info
2. [X] Create an API
   1. [X] Establish router using necessary libraries
   2. [X] Convert the above retrieval function into a GET endpoint
   3. [X] Convert returned struct into JSON
3. [X] Test endpoints with Postman
4. [X] Setup AWS API Gateway and AWS Lambda to serve API
   1. [ ] Create and configure a Lambda function in Golang to perform operations on a DynamoDB table
   2. [ ] Create a REST API in API Gateway to connect to the Lambda function
   3. [ ] Create a DynamoDB table and test it with your Lambda function in the console.
   4. [ ] Deploy your API and test the full setup using Postman in a terminal


### Front-end (HTML, Javascript, Tailwind)
1. [ ] Create a front-end to display the random attraction the client GETs
2. [ ] Create "roll again" option to retrieve a (not necessarily different) attraction

## Classes
- Attraction
    - name: String
    - city: String
    - address: String

https://www.gobeyond.dev/packages-as-layers

Question-Driven Development (QDD)
- Think of an end goal and google your way to success
