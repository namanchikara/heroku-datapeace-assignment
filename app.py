from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mysqldb import MySQL
from sqlalchemy import desc
import json
from operator import itemgetter

app = Flask(__name__)

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User

def tuple_to_jsonString(user):
    return '{' + '"id":{}, \
    "first_name":"{}", \
    "last_name":"{}", \
    "company_name":"{}", \
    "city":"{}",\
    "state":"{}", \
    "zip":{}, \
    "email":"{}", \
    "web":"{}", \
    "age":{}'.format(*user) + '}'



@app.route('/api/users', methods = ['GET', 'POST'])
def Index():
    if request.method == 'GET':
        #################
        # Return list of all users in database with status code 200
        #################

        # = * =
        # extract parameters from the request using `request.args`
        # = * =

        # 0 base index; `page` refers to Pagination
        page = request.args.get('page', default = 1, type = int) - 1
        # value of `name` will be searched as a substring in both `first_name` and `last_name` of all users
        name = request.args.get('name', default = '', type = str)
        # `limit` refers to number of users that need to be sent in Response object
        limit = request.args.get('limit', default = 5, type = int)
        # `sort` refers to the attribute in db, relative to which sorting needs to be performed on Response object, default will be id of user
        sort = request.args.get('sort', default = 'id', type = str)


        # = * =
        # if `-` is prefix in `sort` then sorting will be done in reverse order, and `-` shall be removed from the sort variable.
        # = * =
        if sort[0] == '-':
            reverse_flag = True
            # eg. sort = '-age' will change to sort = 'age'
            sort = sort[1:]
        else:
            reverse_flag = False

        # `que1` -> query1 will filter those users which contain `name` as a substring in `first_name` and `que2` will do the same on `last_name` attribute.
        que1 = User.query.filter(User.first_name.contains(name))
        que2 = User.query.filter(User.last_name.contains(name))
        # `que3` will merge/union results of above two queries
        que3 = que1.union(que2)

        # Fetching the users from database and storing them in data variable
        # data will store a list of tuples, where each element of list corresponds to an user, and each tuple corresponds to the data in i'th element of the list
        data = db.session.execute(que3).fetchall()

        sorting_flag = True
        if name=='' and sort == 'id':
            data.sort(key = lambda k: k[0], reverse = reverse_flag)
            sorting_flag = False

        # For Pagination, We find the first offset (page*limit) and include next `limit` users for Response object
        data = data[page*limit: page*limit + limit]

        # string will be used to store the required user data in String format which will later on be converted into json using json.loads() function
        string = '[ '
        # each user in data will be of tuple type hence, it needs to be converted in string->json
        for user in data:
            string += tuple_to_jsonString(user) + ','
        string = string[:-1] + ']'

        # convert the required data in Json format
        data = json.loads(string)
        del string
        # sort the data according to `sort` variable and reverse_flag's value.

        if sorting_flag:
            data.sort(key = itemgetter(sort), reverse = reverse_flag)

        # return Status code 200 along with data in json format.
        return jsonify(data)

    if request.method == 'POST':
        ################
        # Add new user to database
        ################
        try:
            # retrieve json data from the request
            user = request.get_json()
            # create a `User` object using `user` values
            data = User(user['id'],user['first_name'],user['last_name'],user['company_name'],user['city'],user['state'],user['zip'],user['email'],user['web'],user['age'])
            db.session.add(data)
            db.session.commit()
            # Respond with 201 status code (success)
            return Response("{}", status=201,  mimetype='application/json')
        except:
            # if any attribute is missing (id, first_name, etc..) or not able to add user in database then respond with 409 error code (Conflict)
            return Response("Expected json data for 1 user, got more or less OR user with given ID already exists in db", status = 409)


@app.route('/api/users/<string:id_data>', methods = ['DELETE', 'PUT', 'GET'])
def delete(id_data):
    if request.method == 'DELETE':
        try:
            # Search for user with id = `id_data`
            query = User.query.filter_by(id=id_data)
            d1 = db.session.execute(query).first()
            if d1:
                # User found then, delete it
                User.query.filter_by(id=id_data).delete()
                db.session.commit()
                # User deleted from the db.
                return Response("{}", status = 200)
            else:
                # User not found, Can't delete
                return Response("{}", status = 404)

        except:
            return Response("{}", status = 404)

    if request.method == 'GET':
        try:
            # Search for user with id = `id_data`
            query = User.query.filter_by(id=id_data)
            data = db.session.execute(query).first()
            # try to convert data i.e of tuple type into jsonString -> json type.
            data = json.loads(tuple_to_jsonString(data))
            return jsonify(data)
        except:
            # User with provided ID not found in database
            return Response("{}", status = 404)

    if request.method == 'PUT':
        try:
            # Search for user
            query = User.query.filter_by(id=id_data).first()
            # load json from request
            data = request.get_json()
            for key in data:
                # Doesn't allow users to change their id
                if key == 'id':
                    pass
                # Update info
                setattr(query, key, data[key])
            # commit to db
            db.session.commit()
            return Response("{}", status = 200)

        except:
            # User not found in db
            return Response("{}", status = 404)

@app.route('/api/test/multipleUsers', methods = ['POST','DELETE'])
def add():
    if request.method == 'POST':
        ################
        # This api is to add multiple users in one go, simply copy the whole sample data and POST it,
        # Basically built it to populate the db for testing purposes.
        ################
        data = request.get_json()
        for user in data:
            try:
                toadd = User(user['id'],user['first_name'],user['last_name'],user['company_name'],user['city'],user['state'],user['zip'],user['email'],user['web'],user['age'])
            except:
                print('\n\n\n')
                print(type(data))

            try:
                db.session.add(toadd)
                db.session.commit()
            except:
                # User already exists in db.
                pass

        return Response("{}", status = 201)
    if request.method == 'DELETE':
        db.drop_all()
        db.create_all()
        return Response("{}", status = 200)
