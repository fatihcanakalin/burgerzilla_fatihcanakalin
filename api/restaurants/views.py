from curses.ascii import HT
from flask_restx import Namespace,Resource,fields
from flask_jwt_extended import jwt_required,get_jwt_identity
import jwt
from sqlalchemy import Integer
from ..models.menus import Menu
from ..models.orders import Order, OrderStatus
from ..models.users import User
from ..models.restaurants import Restaurant
from ..models.products import Product
from http import HTTPStatus
from ..utils.db import db


restaurant_namespace = Namespace('restaurants',description="Namespace for restaurants")

menu_model = restaurant_namespace.model(
    'Menu',{
        "id":fields.Integer(),
        "name":fields.String(description="name of restaurant's menu", required=True)
    }
)

product_model = restaurant_namespace.model(
    'Product',{
        "id":fields.Integer(),
        'name':fields.String(description="name of product",required=True),
        "description":fields.String(),
        "price":fields.Float()
    }
)

order_model = restaurant_namespace.model(
    "Order",{
        "quantity":fields.Integer(),
         "user_id":fields.Integer(),
         "product_id":fields.Integer(),
         'order_status':fields.String(description="The status of Order",
            required=True, enum=[e.name for e in OrderStatus]
        )
    }
)


# add new menu to restaurant
@restaurant_namespace.route('/create-menu')
class CreateMenu(Resource):
    
    @restaurant_namespace.expect(menu_model)
    @restaurant_namespace.marshal_with(menu_model)
    @restaurant_namespace.doc(
        description="This method create a new menu and accept application/JSON format for the operation with 'name' is the only and the required parameter for the JSON."
    )
    @jwt_required()
    def post(self):
        """
            Create a new menu 
        """

        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        
        # store the input in the current request
        data = restaurant_namespace.payload

        # create a new menu with Menu Class
        new_menu = Menu(
            name = data['name']
        )
        
        # query for restaurant id
        rest = Restaurant.query.filter_by(user_id=current_user.id).first()
        new_menu.restaurant_id = rest.id

        # save to database
        new_menu.save()

        return new_menu, HTTPStatus.CREATED


# list all orders
@restaurant_namespace.route('/restaurant/<int:restaurant_id>/orders')
class ListAllOrders(Resource):
    
    @restaurant_namespace.marshal_list_with(order_model)
    @restaurant_namespace.doc(
        description="This method returns all specific restaurant orders available in database in JSON format.",
        params={
            "restaurant_id":"A restaurant ID"
        }
    )
    @jwt_required()
    def get(self,restaurant_id):
        """
            Get all orders
        """
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()
        
        restaurant = Restaurant.get_by_id(restaurant_id)
        menus = Menu.query.filter_by(restaurant_id=restaurant.id).first()
        products = Product.query.filter_by(menu_id=menus.id).all()

        for product in products:
           orders = Order.query.filter_by(product_id=product.id).all()
           # if product is already ordered and user is this restaurant employee return orders
           if orders != [] and restaurant.user_id==current_user.id:
               return orders, HTTPStatus.OK


# order detail (burayi daha sonra kontrol et)
@restaurant_namespace.route('/restaurant/order/<int:order_id>')
class OrderDetail(Resource):

    @restaurant_namespace.marshal_with(order_model)
    @restaurant_namespace.doc(
        description="This method returns specific order detail availabile in database in json format",
        params={
            "order_id":"An order ID"
        }
    )
    @jwt_required()
    def get(self, order_id):
        """
            Order detail
        """
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()
        restaurant = Restaurant.query.filter_by(user_id=current_user.id).first()
        order = Order.get_by_id(order_id)

        if restaurant.user_id == current_user.id:
            return order, HTTPStatus.OK

# cancel an order and change status by restaurant
@restaurant_namespace.route('/restaurant/order/status/<int:order_id>')
class CancelUpdateOrderStatus(Resource):

    @restaurant_namespace.marshal_with(order_model)
    @restaurant_namespace.doc(
        description = "This method update and cancel order status",
        params={
            "order_id":"customer's order_id"
        }
    )
    @jwt_required()
    def patch(self,order_id):
        """
            Cancel an order by restaurant (Update Order Status by Restaurant)
        """
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        data = restaurant_namespace.payload

        order_to_update = Order.get_by_id(order_id)
        
        order_to_update.order_status = data['order_status']

        if current_user.is_restaurant_employee:
            db.session.commit()

            return order_to_update, HTTPStatus.OK



# get menu detail and update menu
@restaurant_namespace.route('/restaurant/menus/<int:menu_id>')
class GetUpdateMenuDetail(Resource):

    @restaurant_namespace.marshal_with(menu_model)
    @restaurant_namespace.doc(
        description="This method returns menu detail of restaurant",
        params={
            "menu_id":"menu ID of restaurant"
        }
    )
    @jwt_required()
    def get(self, menu_id):
        """
            Get menu detail with id
        """
        menu = Menu.get_by_id(menu_id)

        return menu, HTTPStatus.OK

    @restaurant_namespace.marshal_with(menu_model)
    @restaurant_namespace.doc(
        description="This method update menu of restaurant that available in database",
        params={
            "menu_id":"menu ID of restaurant"
        }
    )
    @jwt_required()
    def put(self, menu_id):
        """
            Update menu with id
        """
        menu_to_update = Menu.get_by_id(menu_id)

        data = restaurant_namespace.payload

        menu_to_update.name = data['name']

        db.session.commit()

        return menu_to_update, HTTPStatus.OK


# list all menu items
@restaurant_namespace.route('/restaurant/menus/<int:menu_id>/products')
class ListMenuItems(Resource):

    @restaurant_namespace.marshal_with(menu_model)
    @restaurant_namespace.doc(
        description="This method returns all products of menu availabile in database in json format",
        params={
            "menu_id":"menu_id of restaurant's menu"
        }
    )
    @jwt_required()
    def get(self, menu_id):
        """
            List all menu items
        """
        menu = Menu.get_by_id(menu_id)

        return menu.products, HTTPStatus.OK
        


#add a item to menu
@restaurant_namespace.route('/restaurant/menus/<int:menu_id>/add-item')
class AddItem(Resource):

    
    @restaurant_namespace.expect(product_model)
    @restaurant_namespace.marshal_with(product_model)
    @restaurant_namespace.doc(
        description="This method add a new product in menu",
        params={
            "menu_id":"menu_id of restaurant in order to add new product"
        }
    )
    @jwt_required()
    def post(self, menu_id):
        """
            Add a item to menu
        """
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        data = restaurant_namespace.payload

        new_product = Product(
            name = data['name'],
            price = data['price'],
            description = data['description']
        )

        # product foreign key value
        new_product.menu_id = menu_id

        if current_user.is_restaurant_employee:
            new_product.save()

        return new_product, HTTPStatus.CREATED



# get menu's item detail, update and delete menu's item
@restaurant_namespace.route('/restaurant/menus/<int:menu_id>/product/<int:product_id>')
class GetPutDeleteMenuItem(Resource):
    
    @restaurant_namespace.marshal_with(product_model)
    @restaurant_namespace.doc(
        description="This method returns menu's product detail availabile in database in json format",
        params={
            "menu_id":"A menu ID of restaurant",
            "product_id":"A product ID"
        }
    )
    @jwt_required()
    def get(self, menu_id, product_id):
        """
            Get menu's item detail
        """
        menu = Menu.get_by_id(menu_id)
        product = Product.get_by_id(product_id)

        product_detail = product.query.filter_by(id=product_id).filter_by(menu_id=menu.id).first()

        return product_detail, HTTPStatus.OK

    @restaurant_namespace.expect(product_model)
    @restaurant_namespace.marshal_with(product_model)
    @restaurant_namespace.doc(
        description="This method updates menu's product availabile in database in json format",
        params={
            "menu_id":"A menu ID of restaurant",
            "product_id":"A product ID"
        }
    )
    @jwt_required()
    def put(self, menu_id, product_id):
        """
            Update menu's item
        """
        menu = Menu.get_by_id(menu_id)

        product = Product.get_by_id(product_id)

        product_to_update = product.query.filter_by(id=product_id).filter_by(menu_id=menu.id).first()

        data = restaurant_namespace.payload

        product_to_update.name = data['name']
        product_to_update.description = data['description']
        product_to_update.price = data['price']

        db.session.commit()

        return product_to_update, HTTPStatus.OK



    @restaurant_namespace.marshal_with(product_model)
    @restaurant_namespace.doc(
        description="This method delete menu's product availabile in database in json format",
        params={
            "menu_id":"A menu ID of restaurant",
            "product_id":"A product ID"
        }
    )
    @jwt_required()
    def delete(self, menu_id, product_id):
        """
            Delete menu's item
        """
        
        menu = Menu.get_by_id(menu_id)

        product = Product.get_by_id(product_id)

        product_to_delete = product.query.filter_by(id=product_id).filter_by(menu_id=menu.id).first()

        product_to_delete.delete()

        return product_to_delete, HTTPStatus.NO_CONTENT



