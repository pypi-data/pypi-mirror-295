"""
* MTGJSON Schema: Foreign Data
* https://mtgjson.com/data-models/foreign-data/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema


class ForeignData(Schema):
    """Model describing the properties for a card in alternate languages."""
    faceName: Optional[str] = None
    flavorText: Optional[str] = None
    language: str
    multiverseId: Optional[int] = None
    name: str
    text: Optional[str] = None
    type: Optional[str] = None