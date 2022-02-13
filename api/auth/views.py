from flask_restx import Namespace,Resource,fields
from flask import request
from ..models.users import User
from ..models.restaurants import Restaurant
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Conflict, BadRequest

"""
Signup, login and create a new restaurant account
"""

# namespace for authentication
auth_namespace=Namespace('auth', description="a namespace for authentication")


# is_restaurant_employee return False as a default
signup_model = auth_namespace.model(
    'SignUp',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="username"),
        'first_name':fields.String(required=True,description="firstname of user"),
        'last_name':fields.String(required=True,description="lastname of user"),
        'email':fields.String(required=True,description="email of user"),
        'password':fields.String(required=True,description="A password"),
        'is_restaurant_employee':fields.Boolean(required=True,description="This field shows that user is owner of restaurant or staff",default=False)
    }
)


# return user_model after creating a user account
user_model = auth_namespace.model(
    'User',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="username"),
        'first_name':fields.String(required=True, description="firstname of user"),
        'last_name':fields.String(required=True,description="lastname of user"),
        'email':fields.String(required=True,description="email of user"),
        'password_hash':fields.String(required=True,description="A password"),
        'is_active':fields.Boolean(description="This field shows that user is active or not"),
        'is_restaurant_employee':fields.Boolean(required=True,description="This field shows that user is owner of restaurant or staff",default=False)
    }
)


# login model
login_model = auth_namespace.model(
    'Login',{
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True, description="user password")
    }
)

#restaurant model
restaurant_model = auth_namespace.model(
    'Restaurant',{
        'id':fields.Integer(),
        'name':fields.String(required=True,description="name of restaurant")
    }
)


# create a user account
@auth_namespace.route('/signup')
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
            Create a new user account
        """
        # returns data as json
        data = request.get_json()

        try:
        # create a new user with User class
            new_user = User(
                username = data.get('username'),
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
                email = data.get('email'),
                password_hash = generate_password_hash(data.get('password')),
                is_restaurant_employee = data.get('is_restaurant_employee')
            )

            # save to user to the database
            new_user.save()

            return new_user, HTTPStatus.CREATED

        except Exception as e:
            raise Conflict(f"User with email {data.get('email')} exists!")



# login 
@auth_namespace.route('/login')
class Login(Resource):
    
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate a JWT pair
        """

        data = request.get_json()

        # login 
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        # if user is exist and password is correct return access token
        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)

            response = {
                'access_token': access_token
            }


            return response, HTTPStatus.OK

        raise BadRequest("Invalid username or password!")



@auth_namespace.route('/create-restaurant')
class CreateRestaurant(Resource):

    @auth_namespace.expect(restaurant_model)
    @auth_namespace.marshal_list_with(restaurant_model)
    @jwt_required()
    def post(self):

        """
            Create a restaurant account
        """

        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        # parse data come from client as a json format
        data = request.get_json()

        # restaurant object from Restaurant class
        new_restaurant= Restaurant(
            name = data.get('name'),
        )

        # assign user_id value in restaurant's foreign key
        new_restaurant.user_id = current_user.id

        # if user is a restaurant employee then save to database
        if current_user.is_restaurant_employee:

            # save new_restaurant into database
            new_restaurant.save()

            return new_restaurant, HTTPStatus.CREATED

        raise BadRequest("Your account is not related with restaurant")






        


        
