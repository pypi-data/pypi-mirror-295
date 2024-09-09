"""
* MTGJSON Schema: Related Cards
* https://mtgjson.com/data-models/related-cards/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema


class RelatedCards(Schema):
    """Model describing the properties of a card that has relations to other cards."""
    reverseRelated: Optional[list[str]] = None
    spellbook: Optional[list[str]] = None
