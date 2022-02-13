from email import header
import unittest
from urllib import response
from .. import create_app
from ..utils.db import db
from ..config.config import config_dict
from flask_jwt_extended import create_access_token


class RestaurantTestCase(unittest.TestCase):

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


    # test get menu detail
    def test_get_menu_detail(self):
        token = create_access_token(identity='testuser')

        # authorization header pass jwt

        headers = {
            "Authorization":f"Bearer {token}"
        }


        response = self.client.get('restaurants/restaurant/menu/<int:menu_id>',headers=headers)


        # there is no data in database so return 404
        assert response.status_code == 404

        assert response.json == None


    # test get menu's item detail

    def test_get_menu_item_detail(self):

        token = create_access_token(identity='testuser')

        # authorization header pass jwt

        headers = {
            "Authorization":f"Bearer {token}"
        }

        response = self.client.get('restaurants/restaurant/menu/<int:menu_id>/product/<int:product_id>',headers=headers)


        assert response.status_code == 404


    # list menu's all items
    def test_list_menu_items(self):

        token = create_access_token(identity='testuser')

        # authorization header pass jwt

        headers = {
            "Authorization":f"Bearer {token}"
        }

        response = self.client.get('restaurants/restaurant/menu/<int:menu_id>/products',headers=headers)


        assert response.status_code == 404


    # order detail
    def test_order_detail(self):

        token = create_access_token(identity='testuser')

        # authorization header pass jwt

        headers = {
            "Authorization":f"Bearer {token}"
        }

        response = self.client.get('restaurants/restaurant/order/<int:order_id>',headers=headers)


        assert response.status_code == 404

    # get all orders

    def test_get_all_orders(self):

        token = create_access_token(identity='testuser')

        # authorization header pass jwt

        headers = {
            "Authorization":f"Bearer {token}"
        }

        response = self.client.get('restaurants/restaurant/<int:restaurant_id>',headers=headers)


        assert response.status_code == 404