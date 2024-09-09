"""
* MTGJSON Schema: Deck
* https://mtgjson.com/data-models/deck/
"""
# Standard Library Imports
from typing import Optional, Union

# Third Party Imports
from omnitils.schema import Schema

# Local Imports
from hexproof.mtgjson.schema.card import CardDeck


class Deck(Schema):
    """Model describing the properties of an individual deck."""
    code: str
    commander: Optional[list[CardDeck]] = None
    mainBoard: list[CardDeck] = []
    name: str
    releaseDate: Union[str, None] = None
    sideBoard: list[CardDeck] = []
    type: str
