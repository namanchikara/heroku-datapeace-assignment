# heroku-datapeace-assignment

* Deployed at https://datapeace-assignment.herokuapp.com/api/users

# Technologies used
* Heroku
* Flask
* Flask-sqlAlchemy
* postgres
* json, (demo data from http://demo9197058.mockable.io/users)


# End points
* `/api/test/multipleUsers` - `POST` - To add multiple users 
  1. Post request must send data in `json` format to populate db
  2. Response with HTTP status code `201` on success `{}`

* `/api/test/multipleUsers` - `DELETE` - To delete all users in db

* `/api/users` - `GET` - To list the users. 
  1. Response with HTTP status code `200` on success.
  2. Also, supports some query parameters:-
  3. `page` - a number for pagination
  4. `limit` - no. of items to be returned, default limit is 5
  5. `name` - search user by name as a substring in First Name or Last Name (Note, use substring matching algorithm/pattern to match the name)
  6. `Sort` - name of attribute, the items to be sorted. By default it returns items in ascending order if  this parameter exist, and if the value of parameter is prefixed with ‘-’ character, then it should return items in descending order.
  7. Sample query endpoint:- `/api/users?page=1&limit=10&name=James&sort=-age`. This endpoint should return list of 10 users whose first name or last name contains substring given name and sort the users by age in descending order of page 1.

* `/api/users` - `POST` - To create a new user
  1. Request Payload should be like in json format :-
  2. Response with HTTP status code `201` on success and `{}`
  3. This endpoint will create a new user inside the database

* `/api/users/{id}` - `GET` - To get the details of a user
  1. Here `{id}` will be the id of the user in path parameter 
  2. Response with HTTP status code `200` on success
  3. Sample query looks like:- `/api/users/1` of `GET` type

* `/api/users/{id}` - `PUT` - To update the details of a user
  1. Here `{id}` will be the id of the user in path parameter 
  2. Request Payload should be like in `json` format for updating first name, last name and age:-
  3. Response with HTTP status code `200` on success and `{}`

* `/api/users/{id}` - `DELETE` - To delete the user
  1. Here {id} will be the id of the user in path parameter 
  2. Response with HTTP status code 200 on success `{}`


#### Followed https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc to build this app :)

