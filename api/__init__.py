"""
Application Factory
Help us to create multiple instance of application
"""
from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from .customers.views import customer_namespace
from .auth.views import auth_namespace
from .restaurants.views import restaurant_namespace
from .config.config import config_dict
from .utils.db import db
from .models.menus import Menu
from .models.orders import Order
from .models.products import Product
from .models.restaurants import Restaurant
from .models.users import User
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

def create_app(config=config_dict['development']):
    app = Flask(__name__)

    app.config.from_object(config)

    authorizations={
        "Bearer Auth":{
            'type':"apiKey",
            'in':'header',
            'name':'Authorization',
            'description':"Add a JWT with ** Bearer &lt; JWT&gt; to authorize"
        }
    }

    # api instance comes from FLASK-RESTX
    api = Api(app,
        title="Burgerzilla REST-API",
        description="A REST-API micro-service that takes order from hamburger restaurants, can view the status of the order, and enable transactions with the customer/restaurant",
        authorizations=authorizations,
        security="Bearer Auth"
    )

    # register the namespaces
    api.add_namespace(auth_namespace)
    api.add_namespace(customer_namespace)
    api.add_namespace(restaurant_namespace)

    db.init_app(app)

    migrate=Migrate(app,db)

    jwt = JWTManager(app)

    # error handling with Werkzeug
    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error":"Not Found"},404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error":"Method Not Allowed"},405


    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User':User,
            'Menu':Menu,
            'Order':Order,
            'Product':Product,
            'Restaurant':Restaurant
        }

    return app