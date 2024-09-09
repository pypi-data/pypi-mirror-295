"""
* MTGJSON Schema: Purchase Urls
* https://mtgjson.com/data-models/purchase-urls/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema


class PurchaseUrls(Schema):
    """Model describing the properties of links to purchase a product from a marketplace."""
    cardKingdom: Optional[str] = None
    cardKingdomEtched: Optional[str] = None
    cardKingdomFoil: Optional[str] = None
    cardmarket: Optional[str] = None
    tcgplayer: Optional[str] = None
    tcgplayerEtched: Optional[str] = None
