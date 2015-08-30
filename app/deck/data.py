import json
from app.deck.models import DeckOfCards


class DataManagerMixin(object):

    @staticmethod
    def _serialize_deck_result(database_result):
        return {
            'id': database_result['id'],
            'cards_remaining': len(database_result['deck']['cards_remaining']),
            'cards_removed': len(database_result['deck']['cards_removed'])
        }

    def _select_deck_by_id(self, api_key, deck_id):
        self.cursor.callproc('sp_app_decks_select', [api_key, deck_id, ])
        return self.cursor.fetchone()

    def _update_deck_by_id(self, api_key, deck_id, deck):
        self.cursor.callproc('sp_app_decks_update', [api_key, deck_id, json.dumps(deck), ])
        return self.cursor.fetchone()

    def create_deck(self, api_key, num_of_decks):
        deck = DeckOfCards.generate_deck(count=num_of_decks)
        deck.shuffle()
        self.cursor.callproc('sp_app_decks_insert', [api_key, deck.to_json(), ])
        result = self.cursor.fetchone()
        return self._serialize_deck_result(result[0])

    def list_decks(self, api_key):
        self.cursor.callproc('sp_app_decks_list', [api_key, ])
        result = self.cursor.fetchone()
        return [self._serialize_deck_result(d) for d in result[0]]

    def get_deck(self, api_key, deck_id):
        result = self._select_deck_by_id(api_key, deck_id)
        return self._serialize_deck_result(result[0]) if result else result

    def shuffle_deck(self, api_key, deck_id):
        result = self._select_deck_by_id(api_key, deck_id)
        if not result:
            return None
        deck = DeckOfCards.from_dict(result[0])
        deck.shuffle()
        result = self._update_deck_by_id(api_key, deck_id, deck.to_json())
        return self._serialize_deck_result(result[0]) if result else result

    def draw_cards_from_deck(self, api_key, deck_id, number_cards):
        result = self._select_deck_by_id(api_key, deck_id)
        if not result:
            return None
        deck = result[0]
        cards_drawn = []
        for n in range(number_cards):
            cards_drawn.append(deck['cards']['available'].pop(0))
        deck['cards']['removed'].extend(cards_drawn)
        result = self._update_deck_by_id(api_key, deck_id, deck)
        return {
            'deck': self._serialize_deck_result(result[0]),
            'cards': cards_drawn
        }
