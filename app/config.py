import os


TWO_WEEKS = 1209600
TOKEN_EXPIRES = TWO_WEEKS

SECRET_KEY = os.getenv('SECRET_KEY')
assert SECRET_KEY

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgres://postgres@{0}:5432/postgres'.format(os.getenv('DB_PORT_5432_TCP_ADDR', None)))
assert DATABASE_URL

CARD_IMAGE_PATH = os.getenv('CARD_IMAGE_PATH')
assert CARD_IMAGE_PATH

API_KEY = os.getenv('API_KEY')
assert API_KEY
