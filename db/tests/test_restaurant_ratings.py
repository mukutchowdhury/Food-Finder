# import pytest

# import db.ratings as ratings

# from db.ratings import (
#     REVIEW_ID,
#     RESTAURANT_ID,
#     USER_ID,
#     TEXT,
#     STAR)

# @pytest.fixture(scope='function')
# def test_data():
#     temp_review = ratings._get_test_rating()
#     ret = ratings.add_restaurant_rating(
#         temp_review[REVIEW_ID],
#         temp_review[RESTAURANT_ID],
#         temp_review[USER_ID],
#         temp_review[TEXT],
#         temp_review[STAR])
#     yield temp_review

#     if ratings.exists(temp_review[REVIEW_ID]):
#         ratings.del_rating(temp_review[REVIEW_ID])


# def test_get_review(test_data):
#     review_id = test_data["restaurant_id"]
#     all_ratings = ratings.get_all_ratings()
#     assert len(all_ratings) > 0
#     for review_id in all_ratings:
#         assert isinstance(review_id, int)
#         assert isinstance(all_ratings[review_id], dict)
#     assert review_id in all_ratings


# def test_get_restaurant_ratings():
#     ratings = restratings.get_ratings()
#     assert isinstance(ratings, dict)
#     assert len(ratings) > 0
#     for restaurant in ratings:
#         assert isinstance(restaurant, str)
#         assert isinstance(ratings[restaurant], dict)


# def test_add_empty_restaurant():
#     with pytest.raises(ValueError):
#         restratings.add_restaurant_rating('', 1, 'some review', 5)

# def test_add_dup_restaurant_rating(temp_rating):
#     dup_name = temp_rating
#     with pytest.raises(ValueError):
#         restratings.add_restaurant_rating(dup_name, 1, 'some review', 5)

# NEW_RESTAURANT_NAME = 'Spicy Sandwiches'


# def test_add_new_restaurant():
#     restratings.add_restaurant_rating(NEW_RESTAURANT_NAME, 4, "Terrible", 1)
#     assert NEW_RESTAURANT_NAME in restratings.get_ratings()