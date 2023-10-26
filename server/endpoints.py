"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask
from flask import request
from flask_restx import Resource, Api

import db.users as users

app = Flask(__name__)
api = Api(app)

HELLO_EP = '/hello'
HELLO_RESP = 'hello'

# MENUS
MAIN_MENU = '/MainMenu'
MAIN_MENU_NM = "Welcome to Food Finder!"
LOGIN_PAGE = '/LoginPage'
LOGIN_SCREEN_MSG = 'Please Login or Register'

# ENDPOINTS
LOGIN_SYSTEM = '/LoginSystem'
REGISTRATION_SYSTEM = '/RegistrationSystem'

TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'
MENU = 'menu'

USER_MENU_EP = '/user_menu'
MAIN_MENU_EP = '/MainMenu'


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
                    '1': {'url': f'{LOGIN_SYSTEM}', 'method': 'get',
                          'text': 'Log-In'},
                    '2': {'url': f'{REGISTRATION_SYSTEM}',
                          'method': 'get', 'text': 'Sign-Up'},
                    'X': {'text': 'Exit'},
                }}


# START OF PROJECT #


@api.route(f'{LOGIN_SYSTEM}')
class LoginSystem(Resource):
    """
    This class handles user authentication using database
    """
    def post(self):
        """
        Handles user login by checking the provided credentials
        """

        data = request.get_json()
        user_email = data.get("user_email")
        user_password = data.get("user_password")

        try:
            if (not isinstance(user_email, str) and
               not isinstance(user_password, str)):
                # no feedback will do until we start working with the front-end
                raise TypeError(
                    "One or more parameters for "
                    "registration are not of type string"
                    )

            # Hardcoded User Database #
            db_users = users.get_users()
            # use bcrypt to hash user_password #
            # hash_password = bcrpyt(user_password, salt) #
            for users_key in db_users:
                user_info = db_users[users_key]
                if (user_info[users.EMAIL] == user_email and
                   user_info[users.PASSWORD] == user_password):
                    return {
                        "SYSTEM_STATUS": "PASSED"
                    }, 200

            return {
                "SYSTEM_STATUS": "FAILED"
            }, 200

        except Exception as error:
            return {
                "SYSTEM_STATUS": "FAILED",
                "ERROR_MESSAGE": str(error)
            }, 406


@api.route(f'{REGISTRATION_SYSTEM}')
class RegistrationSystem(Resource):
    """
    This class handles registration
    """

    def post(self):
        """
        Takes care of login information with the entered data information
        """

        data = request.get_json()
        user_email = data.get("user_email")
        user_password = data.get("user_password")
        user_confirm_password = data.get("user_confirm_password")

        try:
            if (not isinstance(user_email, str) and
               not isinstance(user_password, str) and
               not isinstance(user_confirm_password, str)):
                # no feedback will do until we start working with the front-end
                raise TypeError(
                    "One or more parameters for "
                    "registration are not of type string"
                    )

            if user_password != user_confirm_password:
                raise Exception("Passwords don't match")

            # Hardcoded User Database #
            db_users = users.get_users()
            # use bcrypt to hash user_password #
            # hash_password = bcrpyt(user_password, salt) #
            for users_key in db_users:
                user_info = db_users[users_key]
                if (user_info[users.EMAIL] == user_email):
                    return {
                        "SYSTEM_STATUS": "FAILED"
                    }, 200

            # Create a new record in database once that's up
            return {
                "SYSTEM_STATUS": "PASSED"
            }, 200
        except TypeError as error:
            return {
                "SYSTEM_STATUS": "FAILED",
                "ERROR_MESSAGE": str(error)
            }, 406
        except Exception as error:
            return {
                "SYSTEM_STATUS": "FAILED",
                "ERROR_MESSAGE": str(error)
            }, 406
