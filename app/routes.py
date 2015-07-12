from app import api
from deck import handlers as deck_handlers
from user import handlers as user_handlers


api.add_route('/user', user_handlers.UserCollection())
api.add_route('/deck', deck_handlers.DeckCollection())
