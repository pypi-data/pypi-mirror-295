"""
* MTGJSON Schema: Booster
* https://mtgjson.com/data-models/booster/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema

"""
* Schemas
"""


class BoosterPack(Schema):
    """Model describing the properties of how a Set's booster data may be configured."""
    contents: dict[str, Optional[int]]
    weight: int


class BoosterSheet(Schema):
    """Model describing the properties of how a sheet of printed cards can be configured."""
    allowDuplicates: Optional[bool] = None
    balanceColors: Optional[bool] = None
    cards: dict[str, int]
    foil: bool
    fixed: Optional[bool] = None
    totalWeight: int


class BoosterConfig(Schema):
    """Model describing the properties of how a Booster Pack can be configured."""
    boosters: list[BoosterPack] = []
    boostersTotalWeight: int
    sheets: dict[str, BoosterSheet]


"""
* Types
"""

Booster = dict[str, BoosterConfig]
"""
* A Booster is a data structure with containing property values 
of Booster configurations, and is not a Data Model itself.
"""
