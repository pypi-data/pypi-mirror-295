"""
* MTGJSON Schema: Deck Set
* https://mtgjson.com/data-models/deck-set/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema

# Local Imports
from hexproof.mtgjson.schema.card import CardSetDeck


class DeckSet(Schema):
    """Model Describing the properties of an individual Deck within a Set."""
    code: str
    commander: Optional[list[CardSetDeck]] = None
    mainBoard: list[CardSetDeck] = []
    name: str
    releaseDate: Optional[str] = None
    sealedProductUuids: Optional[list[str]] = None
    sideBoard: list[CardSetDeck] = []
    type: str
