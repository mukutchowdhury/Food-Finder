"""
This module interfaces to our user data.
"""

MIN_USER_NAME_LEN = 1 
MIN_EMAIL_LEN = 5
MIN_PASSWORD_LEN = 6
EMAIL = 'EMAIL'
PASSWORD = 'PASSWORD'


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        -The dictionary should include at least one email in the form of a str.
    """
    users = {
        "Eric Brown": {
           EMAIL: 'app123@gmail.com',
           PASSWORD: 'ericiscool'
        },
        "John Richards": {
            EMAIL: 'ora123@gmail.com',
            PASSWORD: 'JOHN123'
        },
    }
    return users
