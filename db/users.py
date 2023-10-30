"""
This module interfaces to our user data.
"""

MIN_USER_NAME_LEN = 1
MIN_EMAIL_LEN = 1
EMAIL = 'EMAIL'
PASSWORD = 'PASSWORD'

# Eric's password -> ericiscool
# John's password -> JOHN123

users = {
        "User_1": {
            EMAIL: 'app123@gmail.com',
            PASSWORD: (
                b'$2b$12$0AZZGPgP7MCwyGwn7KR58eRWyvsJw8WrnjCqy6n.'
                b'gE9OF8V/ayQ/G'
            )
        },
        "User_2": {
            EMAIL: 'ora123@gmail.com',
            PASSWORD: (
                b'$2b$12$.s3eFLLJqiPzHSUM.0VVAuW3Alt4TJH'
                b'VcxLdLG.k.jnEFGR3X0WwW'
            )
        },
    }


# Updates 'users' with a new user entry
def add_user(user_email: str, user_password: bytes):
    user_key = f'User_{len(users)}'
    users[user_key] = {
        EMAIL: user_email,
        PASSWORD: user_password
    }


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        -The dictionary should include at least one email in the form of a str.
    """
    return users
