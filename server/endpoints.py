"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask
from flask_restx import Resource, Api
# import db.db as db

# import db.users as users

app = Flask(__name__)
api = Api(app)

MAIN_MENU = '/MainMenu'
MAIN_MENU_NM = "Welcome to Food Finder!"

USERS = ''

LOGIN_PAGE = '/LoginPage'
LOGIN_SCREEN_MSG = 'Please Login or Register'

LOGIN_SYSTEM = '/LoginSystem'
REGISTRATION_SYSTEM = '/RegistrationSystem'

TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'
MENU = 'menu'

USER_MENU_EP = '/user_menu'
MAIN_MENU_EP = '/MainMenu'

CLIENT_MENU_EP = '/ClientMenu'
RESTAURANT_MENU_EP = '/RestaurantMenu'


@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {'hello': 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(f'{LOGIN_PAGE}')
@api.route('/')
class LoginPage(Resource):
    """
    Some Comment
    """
    def get(self):
        """
        Some Comment
        """
        return {'Title': LOGIN_SCREEN_MSG,
                'Default': 1,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'Log-In'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'Sign-Up'},
                    'X': {'text': 'Exit'},
                }}


@api.route(f'{LOGIN_SYSTEM}')
class LoginSystem(Resource):
    """
    This class handles user authentication
    """
    def post(self, email, password):
        """
        Handles user login by checking the provided credentials

        :param email: The user's email address.
        :param password: The user's password.

        :return: A login success status.
        """
        
        # Pass email and password as arguments to an operator that will
        # query the database

        return {
            "success": True,
        }


@api.route(f'{REGISTRATION_SYSTEM}')
class RegistrationSystem(Resource):
    """
    Some Comment
    """
    def post(self):
        """
        Some Comment
        """
        return {

        }


@api.route(f'{MAIN_MENU}')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main app menu.
        """
        return {'Title': MAIN_MENU_NM,
                'Default': 1,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'Find Food!'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'Open a Store!'},
                    'X': {'text': 'Exit'},
                }}


@api.route(f'{CLIENT_MENU_EP}')
class ClientMenu(Resource):
    """
    Displays Client Main Menu
    """
    def get(self):
        """
        This method will deliver the client main menu
        """
        return {
        }


@api.route(f'{RESTAURANT_MENU_EP}')
class RestaurantMenu(Resource):
    """
    Displays Restaurant Main Menu
    """
    def get(self):
        """
        This method will deliver the Restaurant main menu
        """
        return {
        }


# @api.route(f'{USERS}')
# class Users(Resource):
#     """
#     This class supports fetching a list of all users.
#     """
#     def get(self):
#         """
#         This method returns all users.
#         """
#         return {
#             TYPE: DATA,
#             TITLE: 'Current USER',
#             DATA: users.get_users(),
#             MENU: USER_MENU_EP,
#             RETURN: MAIN_MENU_EP,
#         }
