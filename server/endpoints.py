"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api, fields

import bcrypt
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

# RESTAURANT_RELATED ENDPOINTS
RESTAURANT_REGISTRATION = '/Restaurant_Registration'
ADD_RESTAURANT_MENUITEM = '/Add_Restaurant_MenuItem'
REMOVE_RESTAURANT_MENUITEM = '/Remove_Restaurant_MenuItem'
SET_RESTAURANT_HOURS = '/Set_Restaurant_Hours'
GET_RESTAURANT_REVIEWS = '/Get_Restaurant_Reviews'
SET_RESTAURANT_OPTIONS = '/Set_Restaurant_Options'

# CLIENT_RELATED ENDPOINTS
GET_RESTAURANT_LIST = '/Get_Restaurant_List'
GET_TRENDING_RESTAURANT_LIST = '/Get_Trending_Restaurant_List'
PROVIDE_REVIEW = '/Provide_Review'
GET_RESTAURANT_INFO = '/Get_Restaurant_Info'

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

login_data = api.model('Authentication', {
    "user_email": fields.String,
    "user_password": fields.String
})

registration_data = api.model('Regisration', {
    "user_email": fields.String,
    "user_password": fields.String,
    "user_confirm_password": fields.String
})


@api.route(f'{LOGIN_SYSTEM}')
class LoginSystem(Resource):
    """
    This class handles user authentication using database
    """
    @api.expect(login_data)
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
            byte_password = user_password.encode('utf-8')

            for users_key in db_users:
                user_info = db_users[users_key]
                if (user_info[users.EMAIL] == user_email and
                   bcrypt.checkpw(byte_password, user_info[users.PASSWORD])):
                    # return a token, some cookie, or create a session for user
                    # load onto a new route
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

    @api.expect(registration_data)
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
            # byte_password = user_password.encode('utf-8')
            # hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())

            for users_key in db_users:
                user_info = db_users[users_key]
                if (user_info[users.EMAIL] == user_email):
                    return {
                        "SYSTEM_STATUS": "FAILED"
                    }, 200

            # Create a new record in database once that's up
            # Store user_email and hased_password

            byte_password = user_password.encode('utf-8')
            hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
            users.add_user(user_email, hashed_password)

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


# CLIENT ENDPOINTS #
@api.route(f'{GET_RESTAURANT_LIST}')
class GenerateRestaurantList(Resource):
    """
    Provides users with a list of restaurants
    """
    def get(self):
        """
        Uses zip code and radius to generate the list
        of restaurants and sends it
        """
        pass


# RESTAURANT ENDPOINTS #
@api.route(f'{RESTAURANT_REGISTRATION}')
class RestaurantRegistration(Resource):
    """
    Handles the registration of restaurants
    """
    def post(self):
        """
        Updates restaurants database with a new
        restaurant entry
        """
        try:
            data = request.get_json()
            rest_name = data.get("rest_name")
            rest_owner_email = data.get("rest_owner_email")
            rest_location_zip = data.get("rest_location_zip")

            pass

        except Exception:
            pass
