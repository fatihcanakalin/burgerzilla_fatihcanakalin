import unittest
from ..config.config import config_dict
from ..utils.db import db
from .. import create_app
from ..models.users import User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app=create_app(config=config_dict['testing'])

        # push application context
        self.appctx = self.app.app_context()

        self.appctx.push()

        # test client
        self.client = self.app.test_client()

        # create database table
        db.create_all()


    # tearDown : remove db tables, and set all values as none
    def tearDown(self):
        # drop all database table
        db.drop_all()

        # pop up context
        self.appctx.pop()

        self.app = None

        self.client = None


    # test authentication
    # test client helps to make request to certain endpoints
    def test_user_registration(self): 

        # pass data in order to send request

        data = {
            "username":"testuser",
            "first_name":"test",
            "last_name":"user",
            "email":"test@example.com",
            "password":"password"
        }

        # after client make a request, return this response variable
        # self.client.<httpmethod> 

        response = self.client.post('/auth/signup',json=data)

        user = User.query.filter_by(email="test@example.com").first()

        assert user.username == "testuser"

        assert response.status_code == 201


    # test login

    def test_login(self):


        data = {
            "email":"test@example.com",
            "password":"password"
        }

        response = self.client.post('/auth/login',json=data)

        # user doesnt exist in db so return 400 
        assert response.status_code == 400


