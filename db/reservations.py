"""
reservations.py: contains reservations made by users
and stored using restaurant_id as key
"""

USERNAME = 'username'
TIME = 'time'
PARTY_SIZE = 'party_size'

# reservations can be made by users
reservations = {
    'Terrific Tacos': {
        USERNAME: "Jack",
        TIME: '2023-11-08 19:00',
        PARTY_SIZE: 5
    }
}


def get_all_reservations():
    return reservations


def get_rest_reservation(restaurant):
    if restaurant not in reservations:
        raise ValueError("no reservations made for " + restaurant)

    return reservations[restaurant]


def make_reservation(restaurant, user_name, time, party_size):
    if restaurant not in reservations:
        reservations[restaurant] = []

    reservations[restaurant].append({
        USERNAME: user_name,
        TIME: time,
        PARTY_SIZE: party_size
    })
