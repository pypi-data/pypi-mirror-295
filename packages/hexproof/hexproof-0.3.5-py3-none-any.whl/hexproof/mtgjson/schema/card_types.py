"""
* MTGJSON Schema: Card Types
* https://mtgjson.com/data-models/card-types/
"""
# Third Party Imports
from omnitils.schema import Schema

# Local Imports
from hexproof.mtgjson.schema.card_type import CardType


class CardTypes(Schema):
    """Model describing the properties of a Card Data Model that has possible configurations of
        associated subtypes and supertypes."""
    artifact: CardType
    conspiracy: CardType
    creature: CardType
    enchantment: CardType
    instant: CardType
    land: CardType
    phenomenon: CardType
    plane: CardType
    planeswalker: CardType
    scheme: CardType
    sorcery: CardType
    tribal: CardType
    vanguard: CardType
