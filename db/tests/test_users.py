# import db.users as usrs


# def test_get_users():
#     users = usrs.get_users()
#     assert isinstance(users, dict)
#     assert len(users) > 0  
#     for key in users:
#         assert isinstance(key, str)
#         assert len(key) >= usrs.MIN_USER_NAME_LEN
#         user = users[key]
#         assert isinstance(user, dict)
#         assert usrs.EMAIL in user
#         assert usrs.PASSWORD in user
#         assert isinstance(user[usrs.EMAIL], str)
#         assert isinstance(user[usrs.PASSWORD], bytes)
#         assert len(user[usrs.EMAIL]) >= usrs.MIN_EMAIL_LEN
#         # Password is hashed, so we can't check for length here


# ACCOUNT_EMAIL = "Root@root.com"
# ACCOUNT_PASSWORD = "rooted_admin"
# def test_add_users():
#     usrs.add_user(ACCOUNT_EMAIL, ACCOUNT_PASSWORD)
#     new_user = f'User_{len(usrs.get_users())}'
#     assert new_user in usrs.get_users()