import unittest
from .. import create_app
from ..utils.db import db
from ..config.config import config_dict


class MenuTestCase(unittest.TestCase):

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

