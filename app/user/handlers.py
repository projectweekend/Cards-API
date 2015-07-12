import falcon
from app.utils.misc import make_code
from app.user.validation import UserValidationMixin
from app.user.data import DataManagerMixin


class UserCollection(UserValidationMixin, DataManagerMixin):

    def on_post(self, req, res):
        user_doc = req.context['data']
        user_doc['api_key'] = make_code()
        new_user = self.add_user(user_doc)
        if not new_user:
            title = 'Conflict'
            description = 'Email in use'
            raise falcon.HTTPConflict(title, description)
        # Send email here
        res.status = falcon.HTTP_CREATED
