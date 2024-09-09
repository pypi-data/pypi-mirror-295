"""
* MTGJSON Schema: Price
* https://mtgjson.com/data-models/price/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema

"""
* Schemas
"""


class PricePoints(Schema):
    """Model describing the properties of a card's price provider prices."""
    foil: Optional[dict[str, float]] = None
    normal: Optional[dict[str, float]] = None


class PriceList(Schema):
    """Model describing the properties of a card providers list of buying and selling ability."""
    buylist: Optional[PricePoints] = None
    currency: str
    retail: Optional[PricePoints] = None


class PriceListForProvider(Schema):
    """Utility schema for use with the PriceFormats model outlining the possible providers of a PriceList object."""
    cardkingdom: Optional[PriceList] = None
    cardmarket: Optional[PriceList] = None
    cardsphere: Optional[PriceList] = None
    tcgplayer: Optional[PriceList] = None


class PriceFormats(Schema):
    """Model describing the properties of all product formats that the price providers provide."""
    mtgo: Optional[PriceListForProvider] = None
    paper: Optional[PriceListForProvider] = None


"""
* Types
"""

Price = dict[str, PriceFormats]
"""
* A Price is a data structure containing property values of prices for a card, organized by
its uuid, and is not a Data Model itself.
"""