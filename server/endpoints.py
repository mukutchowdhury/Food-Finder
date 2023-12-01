"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus

import bcrypt
import werkzeug.exceptions as wz
from flask import Flask, request
from flask_restx import Api, Resource, fields

import db.menus as menus
import db.ratings as ratings
import db.reservations as reservations
import db.restaurants as restaurants
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
REMOVE_RESTAURANT = '/Remove_Restaurant'
REMOVE_RESTAURANT_RESERVATIONS = '/Remove_Restaurant_Reservations'
REMOVE_RESTAURANT_MENUITEM = '/Remove_Restaurant_MenuItem'
SET_RESTAURANT_HOURS = '/Set_Restaurant_Hours'
GET_RESTAURANT_REVIEWS = '/Get_Restaurant_Reviews'
SET_RESTAURANT_OPTIONS = '/Set_Restaurant_Options'
RESTAURANT_SPECIAL_MEALS = '/Restaurant_Special_Meals'


# CLIENT_RELATED ENDPOINTS
GET_RESTAURANT_LIST = '/Get_Restaurant_List'
GET_TRENDING_RESTAURANT_LIST = '/Get_Trending_Restaurant_List'
PROVIDE_REVIEW = '/Provide_Review'
GET_RESTAURANT_INFO = '/Get_Restaurant_Info'
MAKE_RESERVATION = '/Make_Reservation'

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

menu_item_data = api.model('menu', {
    "restaurent_id": fields.Integer,
    "item_name": fields.String,
    "item_description": fields.String,
    "item_price": fields.Float,
    "item_category": fields.String,
})

login_data = api.model('Authentication', {
    "user_email": fields.String,
    "user_password": fields.String
})

registration_data = api.model('Registration', {
    "user_email": fields.String,
    "user_password": fields.String,
    "user_confirm_password": fields.String
})

restaurant_data = api.model('Register_Restaurant', {
    "rest_id": fields.Integer,
    "rest_name": fields.String,
    "rest_address": fields.String,
    "rest_zipcode": fields.String,
    "rest_owner_id": fields.Integer
})

special_deals = api.model('Special_Deals', {
    "Restaurant_id": fields.Integer,
    "deal_name": fields.String,
    "deal_price": fields.Float
})

review_data = api.model('ratings', {
    'rest_name': fields.String,
    'user_id': fields.Integer,
    'review': fields.String,
    'star': fields.Integer
})

reservation_data = api.model('reservations', {
    'rest_name': fields.String,
    'username': fields.String,
    'time': fields.String,
    'party_size': fields.String
})

rest_info_data = api.model('restaurant_info', {
    'rest_name': fields.String
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
class GetRestaurantList(Resource):
    """
    Provides users with a list of restaurants
    """
    def get(self):
        return restaurants.get_restaurants()

    # @api.expect(restaurant_data)
    # def post(self):
    #     """
    #     Uses zip code and radius to generate the list
    #     of restaurants and sends it
    #     """
    #     data = request.json
    #     zip_code = data.get("rest_zipcode")
    #     RADIUS = 10
    #     zipcode_str = str(zip_code)
    #     if (int(zipcode_str[-2:]) <= 10):
    #         RADIUS = int(zipcode_str[-2:])
    #     nearby_zipcodes = {zip_code: 0}
    #     if RADIUS > 0:
    #         for i in range(1, RADIUS):
    #             nearby_zipcodes[zip_code-i] = 0
    #             nearby_zipcodes[zip_code+i] = 0
    #     else:
    #         for i in range(1, RADIUS):
    #             nearby_zipcodes[zip_code+i] = 0
    #     nearby_restaurants = {}
    #     for zip in nearby_zipcodes:
    #         nearby_restaurant = restaurants.get_nearby_restaurants(zip)
    #         if len(nearby_restaurant) > 0:
    #             nearby_restaurants.append(nearby_restaurant)
    #     if len(nearby_restaurants) == 0:
    #         return (
    #             'No restaurants found nearby in server'), 404
    #     return {nearby_restaurants}, 201


@api.route(f'{REMOVE_RESTAURANT}')
class RemoveResturant(Resource):
    """
    users can remove restaurants
    """
    def post(self):
        data = request.json
        rest_name = data.get('rest_owner_id')

        restaurant_list = restaurants.get_restaurants

        if rest_name not in restaurant_list:
            return (
                'Restaurant not found in server'), 404
        restaurants.del_restaurant(rest_name)
        return {'Removed' + rest_name + 'successfully!'}, 201


@api.route(f'{MAKE_RESERVATION}')
class SetReservation(Resource):
    """
    users can reserve a table at a restaurant
    """
    def post(self):
        data = request.json
        rest_name = data.get('rest_name')
        username = data.get('username')
        time = data.get('time')
        party_size = data.get('party_size')

        # reservation_list = reservations.get_rest_reservation(rest_name)
        restaurant_list = restaurants.get_restaurants

        if rest_name not in restaurant_list:
            return (
                'Restaurant not found in server'), 404
        reservations.make_reservation(rest_name, username, time, party_size)
        return {'Reservation made for' + rest_name + 'successfully!'}, 201


@api.route(f'{REMOVE_RESTAURANT_RESERVATIONS}')
class RemoveResturantReservations(Resource):
    """
    users can cancel all restaurant reservations
    """
    def post(self):
        data = request.json
        rest_name = data.get('rest_owner_id')

        reservation_list = reservations.get_all_reservations

        if rest_name not in reservation_list:
            return (
                'Restaurant not found in server'), 404
        reservations.del_reservations(rest_name)
        return {'Cancelled' + rest_name + 'reservations successfully!'}, 201


@api.route(f'{PROVIDE_REVIEW}')
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class WriteReview(Resource):
    """
    Handles clients writing reviews on restaurants
    """

    @api.expect(restaurant_data)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        update ratings with custumer reviews
        """
        data = request.json
        restuarant_name = data.get('restaurant_name')
        user_id = data.get('user_id')
        review = data.get('review')
        star = data.get('star')

        restratings = ratings.get_ratings()

        if (not isinstance(restuarant_name, str) and
                not isinstance(user_id, int) and
                not isinstance(review, str) and
                not isinstance(star, int)):
            return {'Please enter valid information'}, 400
        if restuarant_name not in restratings:
            return {'the restaurant is not on our server'}, 404
        else:
            try:
                new_id = ratings.add_restaurant_rating(
                    restuarant_name,
                    user_id,
                    review,
                    star)
                if new_id is None:
                    raise wz.ServiceUnavailable('We have a technical problem.')
                return {'review added successfully!'}, 201
            except ValueError as e:
                raise wz.NotAcceptable(f'{str(e)}')


# get restaurant information for a client
@api.route(f'{GET_RESTAURANT_INFO}')
class GETRESTAURANTINFO(Resource):
    """
    Gets restaurant information that the client request for
    """
    @api.expect(rest_info_data)
    def get(self):
        data = request.get_json()
        rest_name = data.get("rest_name")

        restaurant_list = restaurants.get_list
        if rest_name not in restaurant_list:
            return (
                'Restaurant not found'), 404
        rest_info = restaurants.get(rest_name)
        return rest_info


# RESTAURANT ENDPOINTS #
@api.route(f'{RESTAURANT_REGISTRATION}')
class RestaurantRegistration(Resource):
    """
    Handles the registration of restaurants
    """
    @api.expect(restaurant_data)
    def post(self):
        """
        Updates restaurants database with a new
        restaurant entry
        """
        try:
            data = request.get_json()
            rest_id = data.get("rest_id")
            rest_name = data.get("rest_name")
            rest_address = data.get("rest_address")
            rest_location_zip = data.get("rest_zipcode")
            rest_owner_id = data.get("rest_owner_id")
            restaurants.add_restaurant(
                rest_id,
                rest_name,
                rest_address,
                rest_location_zip,
                rest_owner_id
            )

            return {
                "SYSTEM_STATUS": "PASSED"
                }, 200
        except ValueError as error:
            return {
                "SYSTEM_STATUS": "FAILED",
                "ERROR_MESSAGE": str(error)
            }, 406


# Add Restaurant Menu Items REFRACTORING
@api.route(f'{ADD_RESTAURANT_MENUITEM}')
class AddRestaurantMenuItem(Resource):
    @api.expect(menu_item_data)
    def post(self):
        """
        Adds new menu item to the restaurant's menu
        """
        try:
            data = request.json
            restaurant_id = data['restaurant_id']
            item_name = data['item_name']
            item_description = data['item_description']
            item_price = data['item_price']
            item_category = data['item_category']

            menus.add_item_to_menu(restaurant_id, {
                'item_name': item_name,
                'item_description': item_description,
                'item_price': item_price,
                'item_category': item_category
            })
            return {
                "SYSTEM_STATUS": "PASSED"
            }, 200
        except ValueError as error:
            return {
                "SYSTEM_STATUS": "FAILED",
                "ERROR_MESSAGE": str(error)
            }, 406


# Remove Restaurant Menu Items
@api.route(f'{REMOVE_RESTAURANT_MENUITEM}')
class RemoveRestaurantMenuItem(Resource):
    @api.expect(menu_item_data)
    def post(self):
        """
        removes item from the list
        """
        try:
            data = request.json
            restaurant_id = data['restaurant_id']
            item_name = data['item_name']
            menus.remove_item_from_menu(restaurant_id, item_name)
            return {"MENU_STATUS": "PASS", "message": "Items removed"}, 200
        except ValueError as error:
            return {"MENU_STATUS": "FAIL", "ERROR_MESSAGE": str(error)}, 406


# Set options for restaurant
@api.route(f'{SET_RESTAURANT_OPTIONS}')
class SetRestaurantHours(Resource):
    """
    set the options for the restaurant
    """
    @api.expect(restaurant_data)
    def post(self):
        data = request.json
        rest_name = data.get('rest_name')
        rest_address = data.get('rest_address')
        rest_hours = data.get('rest_hours')

        # reservation_list = reservations.get_rest_reservation(rest_name)
        restaurant_list = restaurants.get_restaurants

        if rest_name not in restaurant_list:
            return (
                'Restaurant not found in server'), 404
        reservations.make_reservation(rest_name, rest_address)
        return {'Reservation made for' + rest_name + 'at time' + rest_hours +
                'added successfully!'}, 201


# Set special menus for restaurant
@api.route(f'{RESTAURANT_SPECIAL_MEALS}')
class Restaurant_Special_Meals(Resource):
    @api.expect(special_deals)
    def put(self):
        try:
            data = request.json
            restaurant_id = data['restaurant_id']
            item_name = data['item_name']
            item_price = data['item_price']
            menus.special_deal_update_price(
                restaurant_id, item_name, item_price)
            return {
                "SYSTEM_STATUS": "PASSED"
            }, 200
        except ValueError as error:
            return {
                "SYSTEM_STATUS": "FAILED",
                "ERROR_MESSAGE": str(error)
            }, 406
