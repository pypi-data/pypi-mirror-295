"""
* MTGJSON Schema: Keywords
* https://mtgjson.com/data-models/keywords/
"""
# Third Party Imports
from omnitils.schema import Schema


class Keywords(Schema):
    """Model describing the properties of keywords available to any card."""
    abilityWords: list[str] = []
    keywordAbilities: list[str] = []
    keywordActions: list[str] = []
