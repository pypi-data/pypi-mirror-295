"""
* Scryfall Schema: Catalog
* https://scryfall.com/docs/api/catalogs
"""
# Standard Library Imports
from typing import Literal

# Third Party Imports
from omnitils.schema import Schema


class Catalog(Schema):
    """An object containing an array of Magic datapoints provided by Scryfall."""
    object: Literal['catalog'] = 'catalog'
    uri: str
    total_values: int
    data: list[str]
