from app.utils.database import database_connection

db = database_connection()


class DatabaseCursor(object):

    def process_resource(self, req, resp, resource):
        resource.db = db
        resource.cursor = db.cursor()

    def process_response(self, req, resp, resource):
        resource.cursor.close()
