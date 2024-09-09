"""
* MTGJSON Schema: Source Products
* https://mtgjson.com/data-models/source-products/
"""
# Third Party Imports
from omnitils.schema import Schema


class SourceProducts(Schema):
    """Model describing the uuids for the card version in a Sealed Product."""
    foil: list[str] = []
    nonfoil: list[str] = []
