from fastapi.testclient import TestClient
from main import app

import pytest

class CustomTestClient(TestClient):
    def delete_with_payload(self , **kwargs):
        return self.request(method = "DELETE" , **kwargs)
    
client  = TestClient(app)


#for creating new user account
@pytest.mark.run(order=1)
def test_create_user():
    sample_payload = {
        "username" : "api_test_user",
        "first_name" : "test",
        "last_name" : "user",
        "email" : "testuserfakeemail@gmail.com",
        "password" : "helloworld",
        "confirm_password" : 'helloworld'
    }
    response = client.post('/user' , json= sample_payload)
    assert response.status_code == 201

@pytest.mark.run(order=2)
def test_user_query_creation():
    response = client.get('/user/api_test_user')
    assert response.status_code == 200

@pytest.mark.run(order=3)
def test_user_delete():
    sample_payload = {
        "username" : "api_test_user",
        "password" : "helloworld",
        "confirm_password" : "helloworld"
    }
    response = client.post('/delete-user' , json = sample_payload)
    assert response.status_code == 200

@pytest.mark.run(order=4)
def test_user_query_delete():
    response = client.get('/user/api_test_user')
    assert response.status_code == 404


'''
 first - creates test account
 second - queries test account
 third - delete test account
 fourth - queries for deleted account
'''

#to run test cases : pytest -m run 
#runs the test cases in order