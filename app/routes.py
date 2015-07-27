from app import api
from user import handlers as user_handlers
from deck import handlers as deck_handlers


api.add_route('/user', user_handlers.UserCollection())
api.add_route('/deck', deck_handlers.DeckCollection())
api.add_route('/deck/{deck_id}', deck_handlers.DeckItem())
api.add_route('/deck/{deck_id}/shuffle', deck_handlers.DeckItemShuffle())
api.add_route('/deck/{deck_id}/draw', deck_handlers.DeckItemDraw())
