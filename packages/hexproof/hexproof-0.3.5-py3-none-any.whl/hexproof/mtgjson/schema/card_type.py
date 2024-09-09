"""
* MTGJSON Schema: Card Type
* https://mtgjson.com/data-models/card-type/
"""
# Third Party Imports
from omnitils.schema import Schema


class CardType(Schema):
    """Model describing the properties of any possible subtypes and supertypes of a CardType Data Model."""
    subTypes: list[str] = []
    superTypes: list[str] = []
