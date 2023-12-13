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


# START OF PROJECT #

menu_item_data = api.model('menu', {
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

restaurant_data = api.model('restaurant_ep_post', {
    "rest_name": fields.String,
    "rest_address": fields.String,
    "rest_zipcode": fields.String,
    "rest_owner_id": fields.Integer
})

menuitem_price = api.model('menu_price', {
    "new_price": fields.Float
})

review_data = api.model('ratings', {
    'text': fields.String,
    'star': fields.Integer
})

edit_text = api.model('text_change', {
    'text': fields.String,
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
@api.route('/restaurant/<int:restaurant_id>')
class RestaurantEP(Resource):
    """
    Handles restaurant get and delete
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, restaurant_id: int):
        """
        Gets a restaurant by restaurant id.
        """
        try:
            rest_data = restaurants.get_restuarant(restaurant_id)
            return rest_data
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, restaurant_id: int):
        """
        Deletes a restaurant by restaurant id.
        """
        try:
            restaurants.del_restaurant(restaurant_id)
            return {restaurant_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route('/restaurant/register')
class AddRestaurant(Resource):
    """
    Handles restaurant creation
    """
    @api.expect(restaurant_data)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Create a restaurant entry
        """
        try:
            data = request.get_json()
            rest_name = data.get("rest_name")
            rest_address = data.get("rest_address")
            rest_location_zip = data.get("rest_zipcode")
            rest_owner_id = data.get("rest_owner_id")
            rest_id = restaurants.add_restaurant(
                rest_name,
                rest_address,
                rest_location_zip,
                rest_owner_id
            )
            if rest_id['status'] is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {'restaurant_id': rest_id['restaurant_id']}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route('/restaurant/all')
class GetRestaurants(Resource):
    """
    Handles get restaurants
    """
    def get(self):
        """
        Returns all recorded restaurants
        """
        rest_data = restaurants.get_restaurants()
        return rest_data


@api.route('/restaurants/by-zipcode/<int:zipcode>')
class GetRestaurantsByZipcode(Resource):
    """
    Handles get on nearby restaurants
    NOT FINISHED - GIANFRANCO
    """
    def get(self, zipcode):
        """
        Returns restaurants based on a given zip code
        """
        # rest_data = restaurants.get_nearby_restaurants(zipcode)
        # return {'data': 'Offline'}
        pass


@api.route('/menu/<int:restaurant_id>')
class MenuEP(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, restaurant_id):
        """
        Returns a restaurant's menu
        """
        try:
            menu_data = menus.get_restuarant_menu(restaurant_id)
            return menu_data
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.expect(menu_item_data)
    def post(self, restaurant_id):
        """
        Adds a menu item to an existing restaurant
        """
        try:
            data = request.json
            item_name = data['item_name']
            item_description = data['item_description']
            item_price = data['item_price']
            item_category = data['item_category']

            menu_data = menus.add_item_to_menu(restaurant_id, {
                'item_name': item_name,
                'item_description': item_description,
                'item_price': item_price,
                'item_category': item_category
            })
            if menu_data['status'] is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {
                'restaurant_id': menu_data['restaurant_id'],
                'menuitem_id': menu_data['menuitem_id']
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route('/menu/<int:restaurant_id>/<int:menuitem_id>')
class MenuItemEP(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.expect(menuitem_price)
    def put(self, restaurant_id, menuitem_id):
        """
        Updates the price of an existing menu item
        """
        try:
            data = request.json
            item_price = data['new_price']
            menus.update_item_price(restaurant_id, menuitem_id, item_price)
            return {menuitem_id: f'Updated From {restaurant_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, restaurant_id, menuitem_id):
        """
        Deletes a menuitem from a restaurant
        """
        try:
            menus.del_item_from_menu(restaurant_id, menuitem_id)
            return {menuitem_id: f'Deleted From {restaurant_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route('/review/<int:restaurant_id>/<int:user_id>')
class ReviewEP(Resource):
    """
    Handles clients writing reviews on restaurants
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.expect(review_data)
    def post(self, restaurant_id, user_id):
        """
        Adds a review of restaurant
        """
        try:
            data = request.json
            text = data['text']
            star = data['star']
            data = ratings.add_restaurant_rating(
                restaurant_id,
                user_id,
                text,
                star
            )
            if data['status'] is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {'review_id': data['review_id']}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route('/review/<int:restaurant_id>/<int:review_id>')
class ReviewEdit(Resource):
    """
    Handles clients writing reviews on restaurants
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.expect(edit_text)
    def put(self, restaurant_id, review_id):
        """
        Updates a review of restaurant
        """
        try:
            data = request.json
            text = data['text']
            ratings.update_review_text(restaurant_id, review_id, text)
            return {review_id: f'Updated From {restaurant_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, restaurant_id, review_id):
        """
        deletes a review of restaurant
        """
        try:
            ratings.del_rating(restaurant_id, review_id)
            return {review_id: f'Deleted From {restaurant_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route('/review/<int:restaurant_id>')
class GetAllReview(Resource):
    """
    Handles returning all reviews of a restaurant
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, restaurant_id):
        """
        Returns all reviews of a restaurant
        """
        try:
            data = ratings.get_all_ratings(restaurant_id)
            return data
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route('/hours/<int:restaurant_id>')
class RestaurantHoursEP(Resource):
    """
    get restaurant time
    """
    def get(self, restaurant_id):
        pass

    def post(self, restaurant_id):
        pass

    def put(self, restaurant_id):
        pass

    def delete(self, restaurant_id):
        pass

# Online Orders
