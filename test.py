from app import app
import unittest
from flask import json
import tests
import os

os.chdir(os.getcwd() + '/tests')

def get_json_from_file(file_name):
    jsonString = ''
    with open(file_name,'r') as jsonData:
        for line in jsonData:
            jsonString += line

    return json.loads(jsonString)


'''
    TEST 1       : to depopulate db
    request type : DELETE
    Expected     : status 200
'''
with app.test_client() as test_app:
    response = test_app.delete('/api/test/multipleUsers')
    assert response.status_code == 200
    print("Test 1 : PASSED")



'''
    TEST 2       : to populate db
    request type : POST
    Expected     : status 201
'''
with app.test_client() as test_app:

    response = test_app.post(
        '/api/test/multipleUsers',
        json = get_json_from_file('sample_data.json'),
    )

    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 201
    print("Test 2 : PASSED")


'''
    TEST 3       : '/api/users'
    request type : GET
    Expected     : status 200 AND first 5 users
'''
with app.test_client() as test_app:
    response = test_app.get('/api/users')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200

    recvd_data = json.loads(response.get_data(as_text=True))


    local_data = get_json_from_file('test3.txt')
    assert recvd_data == local_data

    print("Test 3 : PASSED")

'''
    TEST 4       : '/api/users'
    request type : POST
    Expected     : status 409
    'Trying to add user with user id 3 which already exist in db'
'''
with app.test_client() as test_app:
    userData = get_json_from_file('test4.txt')
    response = test_app.post(
        '/api/users',
        json = userData
    )

    assert response.status_code == 409
    print('Test 4 : PASSED')

'''
    TEST 5       : '/api/users/{id} where id will be 32 in this test'
    request type : GET
    Expected     : status 200 AND JSON of user 32
'''
with app.test_client() as test_app:
    response = test_app.get('/api/users/32')
    assert response.status_code == 200

    recvd_data = json.loads(response.get_data(as_text=True))

    local_data = get_json_from_file('test5.txt')

    assert recvd_data == local_data
    print("Test 5 : PASSED")


'''
    TEST 6       : '/api/users/{id} where id will be 32 in this test'
    request type : DELETE
    Expected     : status 200 AND {} as response
'''
with app.test_client() as test_app:
    response = test_app.delete('/api/users/32')
    assert response.status_code == 200

    recvd_data = json.loads(response.get_data(as_text=True))
    assert recvd_data == {}
    print('Test 6 : PASSED')


'''
    TEST 7       : '/api/users/{id} where id will be 32 in this test'
    request type : DELETE
    Expected     : status 404 AND {} as response
    'Trying to delete user with user id 32 which doesn't exist in db'
'''
with app.test_client() as test_app:
    response = test_app.delete('/api/users/32')
    assert response.status_code == 404

    recvd_data = json.loads(response.get_data(as_text=True))
    assert recvd_data == {}
    print('Test 7 : PASSED')


'''
    TEST 8       : '/api/users/{id} where id will be 32 in this test'
    request type : PUT
    Expected     : status 404 AND {} as response
    'Trying to update info of a user with user id 32 which doensn't exist in db'
'''
with app.test_client() as test_app:
    response = test_app.put('/api/users/32',
        json = get_json_from_file('test8.txt')
    )

    assert response.status_code == 404
    recvd_data = json.loads(response.get_data(as_text=True))
    assert recvd_data == {}
    print('Test 8 : PASSED')

'''
    TEST 9       : '/api/users/{id} where id will be 22 in this test'
    request type : PUT
    Expected     : status 200 AND {} as response
    'Trying to update info of a user with user id 22 which exist in db'
'''
with app.test_client() as test_app:
    response = test_app.put('/api/users/22',
        json = get_json_from_file('test8.txt')
    )

    assert response.status_code == 200
    recvd_data = json.loads(response.get_data(as_text=True))
    assert recvd_data == {}
    print('Test 9 : PASSED')

'''
    TEST 10      : '/api/users'
    request type : POST
    Expected     : status 201
    'Trying to add user with user id 32 which doesn't exist in db'
'''
with app.test_client() as test_app:
    userData = get_json_from_file('test10.txt')
    response = test_app.post(
        '/api/users',
        json = userData
    )

    assert response.status_code == 201
    print('Test 10 : PASSED')


'''
    TEST 11      : '/api/users?page=3&limit=7&name=da&sort=-age'
    request type : GET
    Expected     : status 200 and Correct results as stored in test11.txt
    'Trying to fetch users containing 'da' as substring in their first_name OR last_name \
    goto paginate those results using limit=7 and page=3 i.e return USERS 21-28 falling under \
    such category and then sort them according to age in reverse order'
'''
with app.test_client() as test_app:
    response = test_app.get('/api/users?page=3&limit=7&name=da&sort=-age')
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200

    recvd_data = json.loads(response.get_data(as_text=True))

    local_data = get_json_from_file('test11.txt')
    assert recvd_data == local_data

    print("Test 11 : PASSED")
