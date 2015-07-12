from app import api
from deck import handlers as deck_handlers


api.add_route('/deck', deck_handlers.DeckCollection())
