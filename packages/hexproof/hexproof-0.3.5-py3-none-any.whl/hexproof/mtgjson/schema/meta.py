"""
* MTGJSON Schema: Meta
* https://mtgjson.com/data-models/meta/
"""
# Third Party Imports
from omnitils.schema import Schema


class Meta(Schema):
    """Model describing the properties of the MTGJSON application meta data."""
    date: str
    version: str
