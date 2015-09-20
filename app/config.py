import os


API_KEY = os.getenv('API_KEY')
assert API_KEY

CARD_IMAGE_PATH = os.getenv('CARD_IMAGE_PATH')
assert CARD_IMAGE_PATH

DOCKER_COMPOSE_DB_URL = 'postgres://postgres@{0}:5432/postgres'
DOCKER_COMPOSE_DB_ADDR = os.getenv('DB_PORT_5432_TCP_ADDR', None)

DATABASE_URL = os.getenv('DATABASE_URL', DOCKER_COMPOSE_DB_URL.format(DOCKER_COMPOSE_DB_ADDR))
assert DATABASE_URL

DEFAULT_CARDS_CONFIG = {
    'cards': (
        'ACE_SPADES', '2_SPADES', '3_SPADES', '4_SPADES', '5_SPADES', '6_SPADES', '7_SPADES', '8_SPADES', '9_SPADES', '10_SPADES', 'JACK_SPADES', 'QUEEN_SPADES', 'KING_SPADES',
        'ACE_DIAMONDS', '2_DIAMONDS', '3_DIAMONDS', '4_DIAMONDS', '5_DIAMONDS', '6_DIAMONDS', '7_DIAMONDS', '8_DIAMONDS', '9_DIAMONDS', '10_DIAMONDS', 'JACK_DIAMONDS', 'QUEEN_DIAMONDS', 'KING_DIAMONDS',
        'ACE_CLUBS', '2_CLUBS', '3_CLUBS', '4_CLUBS', '5_CLUBS', '6_CLUBS', '7_CLUBS', '8_CLUBS', '9_CLUBS', '10_CLUBS', 'JACK_CLUBS', 'QUEEN_CLUBS', 'KING_CLUBS',
        'ACE_HEARTS', '2_HEARTS', '3_HEARTS', '4_HEARTS', '5_HEARTS', '6_HEARTS', '7_HEARTS', '8_HEARTS', '9_HEARTS', '10_HEARTS', 'JACK_HEARTS', 'QUEEN_HEARTS', 'KING_HEARTS',
    ),
    'image_path': CARD_IMAGE_PATH
}

TWO_WEEKS = 1209600
TOKEN_EXPIRES = TWO_WEEKS
