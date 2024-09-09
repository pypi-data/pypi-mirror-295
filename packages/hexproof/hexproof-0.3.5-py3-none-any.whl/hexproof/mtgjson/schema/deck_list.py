"""
* MTGJSON Schema: Deck List
* https://mtgjson.com/data-models/deck-list/
"""
# Standard Library Imports
from typing import Union

# Third Party Imports
from omnitils.schema import Schema


class DeckList(Schema):
    """Model describing the meta data properties of an individual Deck."""
    code: str
    fileName: str
    name: str
    releaseDate: Union[str, None]
    type: str
