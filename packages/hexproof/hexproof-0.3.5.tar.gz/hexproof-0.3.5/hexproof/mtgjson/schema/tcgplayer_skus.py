"""
* MTGJSON Schema: TCGPlayer SKUs
* https://mtgjson.com/data-models/tcgplayer-skus/
"""
# Third Party Imports
from omnitils.schema import Schema


class TcgplayerSkus(Schema):
    """Model describing the properties of the TCGplayer SKUs for a product."""
    condition: str
    finishes: list[str] = []
    language: str
    printing: str
    productId: str
    skuId: str
