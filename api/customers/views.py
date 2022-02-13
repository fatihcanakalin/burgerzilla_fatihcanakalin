from flask_restx import Namespace,Resource,fields
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..models.menus import Menu
from ..models.orders import Order,OrderStatus
from ..models.users import User
from ..models.restaurants import Restaurant
from ..models.products import Product
from http import HTTPStatus
from ..utils.db import db


#customer_namespace
customer_namespace = Namespace('customers',description="Namespace for customers")

order_model = customer_namespace.model(
    "Order",{
        "quantity":fields.Integer(),
         "user_id":fields.Integer(),
         "product_id":fields.Integer(),
         'order_status':fields.String(description="The status of Order",
            required=True, enum=[e.name for e in OrderStatus]
        )
    }
)

# create a new order
@customer_namespace.route('/order')
class CreateOrder(Resource):

    @customer_namespace.expect(order_model)
    @customer_namespace.marshal_with(order_model)
    @customer_namespace.doc(
        description="This method create a new order"
    )
    @jwt_required()
    def post(self):
        """
            Place a new order
        """
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        data = customer_namespace.payload

        new_order=Order(
            quantity = data["quantity"],
            product_id = data["product_id"]
        )

        new_order.customer = current_user

        new_order.save()
    
        return new_order, HTTPStatus.CREATED

# get a customer's specific order
@customer_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByCustomer(Resource):

    @customer_namespace.marshal_with(order_model)
    @customer_namespace.doc(
        description="This method returns customer's specific order",
        params={
            "user_id":"A user ID of user",
            "order_id":"An order ID"
        }
    )
    @jwt_required()
    def get(self, user_id, order_id):
        """
            Get customer's specific order
        """
        customer = User.get_by_id(user_id)

        order = Order.query.filter_by(id=order_id).filter_by(customer=customer).first()

        return order, HTTPStatus.OK


# Update an order
@customer_namespace.route('/order/update/<int:order_id>')
class UpdateOrder(Resource):

    @customer_namespace.doc(
        description="This method update of user's order",
        params={
            "order_id":"An order ID"
        }
    )
    @jwt_required()
    def put(self, order_id):
        """
            Update an order
        """
        order_to_update  = Order.get_by_id(order_id)

        data = customer_namespace.payload

        order_to_update.quantity = data['quantity']
        order_to_update.product_id = data['product_id']

        db.session.commit()


# Get all orders by a specific user
@customer_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):

    
    @customer_namespace.marshal_with(order_model)
    @customer_namespace.doc(
        description="This method return all orders of specific user",
        params={
            "user_id":"An user ID"
        }
    )
    @jwt_required()
    def get(self, user_id):
        """
            Get all orders by a specific user
        """
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        user = User.get_by_id(user_id)
        print(user)
        print(current_user)

        if user == current_user:
            orders = user.orders

            return orders

# Cancel an order by customer
@customer_namespace.route('/order/cancel-order/<int:order_id>')
class CancelOrder(Resource):

    @customer_namespace.marshal_with(order_model)
    @customer_namespace.doc(
        description="This method cancel order via customer",
        params={
            "order_id":"An order ID"
        }
    )
    @jwt_required()
    def patch(self, order_id):
        """
            Cancel an order by customer (Update as a CANCELED_BY_CUSTOMER)
        """
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        data = customer_namespace.payload

        order_to_update = Order.get_by_id(order_id)

        order_to_update.order_status = data['order_status']
        print(order_to_update.user_id)
        print(current_user)

        if order_to_update.user_id == current_user.id:
            db.session.commit()

            return order_to_update