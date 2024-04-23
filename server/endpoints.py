"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus

import werkzeug.exceptions as wz
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields, Namespace

import db.categories as categories
import db.menus as menus
import db.ratings as ratings
import db.restaurants as restaurants
import db.users as users

import db.form as fm

app = Flask(__name__)
CORS(app)
api = Api(app)

# USER
SIGN_UP = '/signup'
LOGIN = '/login'
SIGNUP_FORM = '/signup-form'

# RESTAURANT
BY_ZIPCODE = '/by_zipcode'
ALL = '/all'
REGISTER = '/register'

HOUR = '/hour'

CATEGORY_EP = '/category'
REVIEW_EP = '/review'
MENU_EP = '/menu'
RESTAURANT_EP = '/restaurants'
USER_EP = '/user'

USER_NS = 'user'
RESTAURANT_NS = 'restaurants'
MENU_NS = 'menu'
REVIEW_NS = 'review'
CATEGORY_NS = 'category'

user = Namespace(USER_NS, 'User')
restaurant = Namespace(RESTAURANT_NS, 'Restaurant')
menu = Namespace(MENU_NS, 'Menu')
review = Namespace(REVIEW_NS, 'Review')
category = Namespace(CATEGORY_NS, 'Category')

api.add_namespace(user)
api.add_namespace(restaurant)
api.add_namespace(menu)
api.add_namespace(review)
api.add_namespace(category)


menu_item_data = api.model('menu', {
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "category": fields.String,
    "image": fields.String,
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

restaurant_hour_option = api.model('hour_option', {
    'open': fields.String,
    'close': fields.String
})

restaurant_data = api.model('restaurant_ep_post', {
    "name": fields.String,
    "address": fields.String,
    "zipcode": fields.String,
    "owner_id": fields.Integer,
    "image": fields.String,
    "phone": fields.String,
    "cuisine": fields.List(fields.String),
    "keywords": fields.List(fields.String),
    "category": fields.List(fields.String),
    "hours": fields.Nested(restaurant_hour_option),
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

category_model = api.model('category', {
    'name': fields.String,
    'description': fields.String
})


@user.route(f'{SIGN_UP}')
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


@user.route(f'{LOGIN}')
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


@user.route('/<string:id>')
class UserDataEP(Resource):
    """
    Handles retrieving user data
    """
    def get(self, id: str):
        """
        Gets user data.
        """
        try:
            result = users.get_userdata(id)
            return result
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@user.route(f'{SIGNUP_FORM}')
class UserForm(Resource):
    """
    Handles retrieving user signup form
    """
    def get(self):
        return fm.get_form()


@restaurant.route('/<string:restaurant_id>')
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
            rest_data = restaurants.get_restaurant(restaurant_id)
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


@restaurant.route(f'{REGISTER}')
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
            if rest_id['restaurant_id'] != restaurants.MOCK_ID:
                ratings.add_restaurant_rating(rest_id['restaurant_id'],
                                              1, "new_entry", 5)
            return {'restaurant_id': rest_id['restaurant_id']}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@restaurant.route(f'{ALL}')
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


@restaurant.route(f'{BY_ZIPCODE}/<string:zipcode>')
class GetRestaurantsByZipcode(Resource):
    """
    Handles get on nearby restaurants
    """
    def get(self, zipcode):
        """
        Returns restaurants based on a given zip code
        """
        rest_data = restaurants.get_restaurants_by_zipcode(zipcode)
        return rest_data


@restaurant.route(f'{HOUR}/<string:restaurant_id>')
class RestaurantHoursEP(Resource):
    """
    Handles updates on restaurant time
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.expect(restaurant_hour_option)
    def put(self, restaurant_id):
        """
        updates restaurant time
        """
        try:
            data = request.json
            open = data['open']
            close = data['close']
            restaurants.update_restaurant_time(restaurant_id, open, close)
            return {'restaurant_hours':
                    f'Time update for {restaurant_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@menu.route('/<string:restaurant_id>')
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
            item_name = data['name']
            item_description = data['description']
            item_price = data['price']
            item_category = data['category']
            item_image = data['image']

            menu_data = menus.add_item_to_menu(restaurant_id, {
                'name': item_name,
                'description': item_description,
                'price': item_price,
                'category': item_category,
                'image': item_image,
            })
            if menu_data['status'] is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {
                'Added_menu_to_restaurant': restaurant_id,
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@menu.route('/<string:menuitem_id>')
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
            menus.update_price(menuitem_id, item_price)
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


@review.route('/<string:restaurant_id>')
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


@review.route('/<string:review_id>')
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


# PATH /category
@category.route('')
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
    @api.expect(category_model)
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

            category_links = {
                'self': '/category',
                'all_categories': '/categories',
                'delete': f'/category/{name}'
            }
            response = {
                'Created': name,
                '_links': category_links
            }
            return response, HTTPStatus.CREATED
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@category.route('/<string:name>')
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
