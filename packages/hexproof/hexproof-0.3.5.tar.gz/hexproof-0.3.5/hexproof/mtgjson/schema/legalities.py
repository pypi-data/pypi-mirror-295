"""
* MTGJSON Schema: Legalities
* https://mtgjson.com/data-models/legalities/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema


class Legalities(Schema):
    """Model describing the properties of legalities of a card in various game play formats."""
    alchemy: Optional[str] = None
    brawl: Optional[str] = None
    commander: Optional[str] = None
    duel: Optional[str] = None
    explorer: Optional[str] = None
    future: Optional[str] = None
    gladiator: Optional[str] = None
    historic: Optional[str] = None
    historicbrawl: Optional[str] = None
    legacy: Optional[str] = None
    modern: Optional[str] = None
    oathbreaker: Optional[str] = None
    oldschool: Optional[str] = None
    pauper: Optional[str] = None
    paupercommander: Optional[str] = None
    penny: Optional[str] = None
    pioneer: Optional[str] = None
    predh: Optional[str] = None
    premodern: Optional[str] = None
    standard: Optional[str] = None
    standardbrawl: Optional[str] = None
    timeless: Optional[str] = None
    vintage: Optional[str] = None
