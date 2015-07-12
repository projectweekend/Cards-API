import json
from psycopg2 import IntegrityError


class DataManagerMixin(object):

    def add_user(self, user_doc):
        try:
            self.cursor.callproc('sp_app_users_insert', [json.dumps(user_doc), ])
        except IntegrityError:
            return False
        return True
