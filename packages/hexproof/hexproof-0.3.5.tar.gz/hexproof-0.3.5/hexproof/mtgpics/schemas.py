"""
* MTGPics Schemas
"""
import yarl
from omnitils.schema import Schema

"""
* Scraped Data Object Schemas
"""


class ScrapedCard(Schema):
    """Represents an MTG 'Card' scraped from MTGPics."""
    class Config:
        arbitrary_types_allowed = True

    # Schema Fields
    number: int
    name: str
    ref: str
    type: str
    url: yarl.URL
    img: yarl.URL
    artist: str | None = None
    subset: str | None = None
    pt: str | None = None


class ScrapedSet(Schema):
    """Represents an MTG 'Set' scraped from MTGPics."""
    code: str | None
    card_count: int
    date: str
    id: str
    name: str
    normalized: str
