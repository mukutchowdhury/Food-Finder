import db.users as current_users


def test_get_users():
    ff_users = current_users.get_users()
    assert isinstance(ff_users, dict)
    assert len(ff_users) > 0  # more than 0 users
    for key in ff_users:
        assert isinstance(key, str)
        assert len(key) >= current_users.MIN_USER_NAME_LEN
        user = ff_users[key]
        assert isinstance(user, dict)
        assert len(current_users.EMAIL) >= current_users.MIN_EMAIL_LEN
        assert isinstance(user[current_users.EMAIL], str)
        assert len(current_users.PASSWORD) >= current_users.MIN_PASSWORD_LEN
        assert isinstance(user[current_users.PASSWORD], str)