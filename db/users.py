"""
This module interfaces to our user data.
"""

MIN_USER_NAME_LEN = 2
EMAIL = 'email'

def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        -The dictionary should include at least one email in the form of a str.
        
    """
    users = {
        "Apple": {
            EMAIL = app123@gmail.com,
        },
        "Orange": {
            EMAIL = ora123@gmail.com,
        },
    }
    return users
