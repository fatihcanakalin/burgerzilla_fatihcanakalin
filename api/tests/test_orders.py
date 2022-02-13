import unittest
from .. import create_app
from ..utils.db import db
from ..config.config import config_dict
from flask_jwt_extended import create_access_token
from ..models.orders import Order


class OrderTestCase(unittest.TestCase):

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


    # test place a order
    def test_create_order(self):

        data = {
            "quantity":3,
            "product_id":2
        }

        token = create_access_token(identity='testuser')

        # authorization header pass jwt

        headers = {
            "Authorization":f"Bearer {token}"
        }

        response = self.client.post('customers/order', json=data,headers=headers)


        assert response.status_code == 201

        orders = Order.query.all()

        assert len(orders) == 1

