Burgerzilla
=============

A REST-API micro-service that takes orders from hamburger restaurants, can view the status of the order,
 and enables transactions with the customer/restaurant.


The project has been developed using Flask- A python Micro-web framework
and other additional packages describe below in Tech Stack Section.

Installation
------------

Before we begin, kindly install following on your system:-

-   [python3.x](http://www.python.org)
-   [Virtualenv](https://virtualenv.pypa.io/en/stable/)

How to Run the App?
-------------------

Enter the project folder and create a virtual environment
``` 
$ python -m venv env 
```

Activate the virtual environment
``` 
$ source env/bin/actvate #On linux Or Unix

$ source env/Scripts/activate #On Windows 
 
```

Install all requirements

```
$ pip install -r requirements.txt
```

Run the project in development
```
$ export FLASK_APP=api/

$ export FLASK_DEBUG=1

$ flask run

```
Or 
``` 
python runserver.py
``` 



REST Endpoints
--------------

There are two major objects in the app:-

-   Customers
-   Restaurants
    *   Menu

The endpoints and the corresponding REST operations are defined as
follows:-

## ROUTES TO IMPLEMENT
| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| -------- | ----- | -------------- | ------- |
| *POST* | ```/auth/signup/``` | _Register new user_ | _All user types_ |
| *POST* | ```/auth/login/``` | _Login User_ | _All user types_ |
| *POST* | ```/customers/order/``` | _Place an order_ | _All user types_ |
| *GET* | ```/customers/user/{user_id}/order/{order_id}``` | _Get customer's specific order_ | _All user types_ |
| *PUT* | ```/customers/order/update/{order_id}``` | _Update an order_ | _All user types_ |
| *GET* | ```/customers/user/{user_id}/orders``` | _Get all orders by a specific user_ | _All user types_ |
| *PUT* | ```/customers/order/cancel-order/{order_id}``` | _Cancel an order by customer_ | _All user types_ |
| *GET* | ```/restaurant/{rastaurant_id}/orders``` | _List all orders_ | _Restaurant type_ |
| *GET* | ```/restaurant/order/{order_id}``` | _Order detail_ | _Restaurant type_ |
| *PUT* | ```/restaurant/order/{order_id}``` | _Cancel an order by restaurant_ | _Restaurant type_ |
| *PUT* | ```/restaurant/order/status/{order_id}``` | _Update order status by restaurant_ | _Restaurant type_ |
| *GET* | ```/restaurant/menus/{menu_id}``` | _Get menu detail_ | _Restaurant type_ |
| *PUT* | ```/restaurant/menus/{menu_id}``` | _Update menu_ | _Restaurant type_ |
| *GET* | ```/restaurant/menus/{menu_id}/products``` | _List all menu items_ | _Restaurant type_ |
| *POST* | ```/restaurant/menus/{menu_id}/add-item``` | _Add a item to menu_ | _Restaurant type_ |
| *GET* | ```/restaurant/menus/{menu_id}/product/{product_id}``` | _Get menu's item detail_ | _Restaurant type_ |
| *PUT* | ```/restaurant/menus/{menu_id}/product/{product_id}``` | _Update a menu's product_ | _Restaurant type_ |
| *DELETE* | ```/restaurant/menus/{menu_id}/product/{product_id}``` | _Delete a menu's product_ | _Restaurant type_ |

Unit Testing Endpoints
----------------------

In this folder (ideally, inside a virtual environment, to keep this from affecting your local Python libraries).

Once you've got all the requirements in place, you should be able to simply run
```
pytest
```

Tech stack
----------

-   [Flask](http://flask.pocoo.org/) - Web Microframework for Python
-   [Flask-restx](https://flask-restx.readthedocs.io/en/latest/) -
    Extension for flask for quickly building REST APIs
-   [Swagger](https://swagger.io/) - Automatic Documentation for the
    REST endpoints
-   [Flask-migrate](https://flask-migrate.readthedocs.io/en/latest/) -
    An extension that handles SQLAlchemy database migrations for Flask
    applications using Alembic.
-   [postgresql](https://www.postgresql.org//)
-   [pytest](https://docs.pytest.org/en/7.0.x/) 



