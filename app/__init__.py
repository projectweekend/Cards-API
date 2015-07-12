import falcon
from middleware.body_parser import JSONBodyParser
from middleware.json_response import JSONResponse
from middleware.database import DatabaseCursor
from utils.database import database_connection


db = database_connection()

middleware = [JSONBodyParser(), JSONResponse(), DatabaseCursor()]

api = falcon.API(middleware=middleware)


import routes
