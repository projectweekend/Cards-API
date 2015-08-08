import falcon
from middleware.body_parser import JSONBodyParser
from middleware.json_response import JSONResponse
from middleware.database import DatabaseCursor
from middleware.validation import RequestValidation
from middleware.api_key import APIKey
from utils.database import database_connection


db = database_connection()

middleware = [
    APIKey(),
    JSONBodyParser(),
    DatabaseCursor(),
    RequestValidation(),
    JSONResponse(),
]

api = falcon.API(middleware=middleware)


import routes
