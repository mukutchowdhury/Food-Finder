"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus

# import bcrypt
import werkzeug.exceptions as wz
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields

import db.categories as categories
import db.menus as menus
import db.options as options
import db.ratings as ratings
# import db.reservations as reservations
import db.restaurants as restaurants
import db.users as users

app = Flask(__name__)
CORS(app)
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


ADD_RESTAURANT = '/restaurant/register'
RESTAURANT_EP = '/restaurant'
RESTAURANT_ALL = '/restaurant/all'
Menu_EP = '/menu'
REVIEW_EP = '/review'
HOUR_EP = '/hour'

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

# UPDATE SCHEMA #
restaurant_data = api.model('restaurant_ep_post', {
    "name": fields.String,
    "address": fields.String,
    "zipcode": fields.String,
    "owner_id": fields.Integer,
    "image": fields.String,
    "phone": fields.String,
    "cuisine": fields.List(fields.String),
    "keywords": fields.List(fields.String),
    "category": fields.List(fields.String)
})

menuitem_price = api.model('menu_price', {
    "new_price": fields.Float
})

review_data = api.model('ratings', {
    'user_id': fields.Integer,
    'text': fields.String,
    'star': fields.Integer
})

edit_text = api.model('text_change', {
    'text': fields.String,
})

restaurant_hour_option = api.model('hour_option', {
    'open_hour': fields.Integer,
    'open_minute': fields.Integer,
    'close_hour': fields.Integer,
    'close_minute': fields.Integer
})

user_signup = api.model('user_signup', {
    'email': fields.String,
    'password': fields.String,
    'fname': fields.String,
    'lname': fields.String,
    'pimage': fields.String,
    'privilege': fields.Integer
})

user_login = api.model('user_login', {
    'email': fields.String,
    'password': fields.String
})

category = api.model('category', {
    'name': fields.String,
    'description': fields.String
})


# USER AUTHENTICATION #

@api.route('/user/signup')
class UserSignupEP(Resource):
    """
    Handles Signup
    """
    @api.expect(user_signup)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Returns Success Status
        """
        data = request.json
        email = data.get('email')
        password = data.get('password')
        fname = data.get('fname')
        lname = data.get('lname')
        pimage = data.get('pimage')
        pimage = "" if pimage is None else pimage
        privilege = data.get('privilege')
        privilege = 0 if privilege is None else privilege
        try:
            users.add_user(email, password, fname, lname, pimage, privilege)
            return {'status': 'ok'}
        except ValueError as e:
            return {'status': str(e)}


@api.route('/user/login')
class UserLoginEP(Resource):
    """
    Handles Login Authentication
    """
    @api.expect(user_login)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Returns Success Status
        """
        data = request.json
        email = data.get('email')
        password = data.get('password')
        try:
            result = users.get_user(email, password)
            return {'status': 'ok', 'userid': result}
        except ValueError as e:
            return {'status': str(e)}


@api.route('/user/<int:id>')
class UserDataEP(Resource):
    """
    Handles retrieving user data
    """
    def get(self, id: int):
        """
        Gets user data.
        """
        result = users.get_userdata(id)
        return result


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
        data = request.get_json()
        try:
            rest_id = restaurants.add_restaurant(data)
            if rest_id['status'] is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            ratings.add_restaurant_rating(ratings.gen_reviewId(),
                                          rest_id['restaurant_id'],
                                          1, "new_entry", 5)
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
        rest_data = restaurants.get_all_restaurants()
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
        rest_data = restaurants.get_restaurants_by_zipcode(zipcode)
        return rest_data


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
                'name': item_name,
                'description': item_description,
                'price': item_price,
                'category': item_category
            })
            if menu_data['status'] is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {
                'Added_menu_to_restaurant': restaurant_id,
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{Menu_EP}/<int:menuitem_id>')
class MenuItemEP(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.expect(menuitem_price)
    def put(self, menuitem_id):
        """
        Updates the price of an existing menu item
        """
        try:
            data = request.json
            item_price = data['new_price']
            menus.update_item_price(menuitem_id, item_price)
            return {'menuitem': f'Updated {menuitem_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, menuitem_id):
        """
        Deletes a menuitem from a restaurant
        """
        try:
            menus.del_item_from_menu(menuitem_id)
            return {'menuitem': f'Deleted From {menuitem_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{REVIEW_EP}/<int:restaurant_id>')
class ReviewEP(Resource):
    """
    Handles clients writing reviews on restaurants
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, restaurant_id):
        """
        Returns all reviews of a restaurant
        """
        try:
            data = ratings.get_restaurant_ratings(restaurant_id)[1:]
            total_star = 4.5
            if (len(data) != 0):
                total_star = sum(int(singleData['star'])
                                 for singleData in data[1:]) / len(data)
            return {'review': data, 'total': total_star}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.expect(review_data)
    def post(self, restaurant_id):
        """
        Adds a review of restaurant
        """
        try:
            data = request.json
            usrid, text, star = data['user_id'], data['text'], data['star']
            data = ratings.add_restaurant_rating(
                restaurant_id, usrid, text, star
            )
            if data['status'] is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {'added_review_to_restaurant': restaurant_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{REVIEW_EP}/<int:review_id>')
class ReviewEdit(Resource):
    """
    Handles clients writing reviews on restaurants
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.expect(edit_text)
    def put(self, review_id):
        """
        Updates a review of restaurant
        """
        try:
            data = request.json
            text = data['text']
            ratings.update_review_text(review_id, text)
            return {'review': f'Updated review {review_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, review_id):
        """
        deletes a review of restaurant
        """
        try:
            ratings.del_rating(review_id)
            return {'review': f'Deleted From {review_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{HOUR_EP}/<int:restaurant_id>')
class RestaurantHoursEP(Resource):
    """
    get restaurant time
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, restaurant_id):
        try:
            data = options.get_restaurant_hour(restaurant_id)
            return data
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.expect(restaurant_hour_option)
    def post(self, restaurant_id):
        """
        sets restaurant time
        """
        try:
            data = request.json
            open = {
                'hour': data['open_hour'],
                'minute': data['open_minute']
            }
            close = {
                'hour': data['close_hour'],
                'minute': data['close_minute']
            }

            status = options.insert_restaurant_hour(restaurant_id,
                                                    open, close)
            if status is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {'restaurant_hours':
                    f'Time Set for {restaurant_id}'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.expect(restaurant_hour_option)
    def put(self, restaurant_id):
        """
        updates restaurant time
        """
        try:
            data = request.json
            open = {
                'hour': data['open_hour'],
                'minute': data['open_minute']
            }
            close = {
                'hour': data['close_hour'],
                'minute': data['close_minute']
            }
            options.update_restaurant_time(restaurant_id, open, close)
            return {'restaurant_hours':
                    f'Time update for {restaurant_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, restaurant_id):
        """
        deletes restaurant time
        """
        try:
            options.delete_restaurant_time(restaurant_id)
            return {'restaurant_hours':
                    f'Deleted time from {restaurant_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route('/category')
class CategoryEP(Resource):
    """
    Handles all actions related category
    """
    def get(self):
        """
        Returns all categories
        """
        result = categories.getCategories()
        return result

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.expect(category)
    def post(self):
        """
        Creates a new category entry
        """
        try:
            data = request.json
            name = data.get('name')
            description = data.get('description')
            result = categories.addCategory(name, description)
            if result is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {'Created': name}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route('/category/<string:name>')
class CategoryDeleteEP(Resource):
    """
    Handles deletion of category
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, name):
        """
        deletes a category
        """
        try:
            categories.deleteCategory(name)
            return {'Deleted': name}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
