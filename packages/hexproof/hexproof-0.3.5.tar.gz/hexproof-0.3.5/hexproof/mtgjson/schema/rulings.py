"""
* MTGJSON Schema: Rulings
* https://mtgjson.com/data-models/rulings/
"""
# Standard Library Imports
from typing import Optional, List

# Third Party Imports
from omnitils.schema import Schema


class Rulings(Schema):
    """Model describing the properties of rulings for a card."""
    date: str
    text: str
