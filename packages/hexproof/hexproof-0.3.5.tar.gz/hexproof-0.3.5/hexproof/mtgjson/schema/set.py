"""
* MTGJSON Schema: Set
* https://mtgjson.com/data-models/set/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema

# Local Imports
from hexproof.mtgjson.schema.booster import Booster
from hexproof.mtgjson.schema.card import CardSet, CardToken
from hexproof.mtgjson.schema.deck_set import DeckSet
from hexproof.mtgjson.schema.sealed_product import SealedProduct
from hexproof.mtgjson.schema.translations import Translations


class Set(Schema):
    """Model describing the properties of an individual set."""
    baseSetSize: int
    block: Optional[str] = None
    booster: Optional[Booster] = None
    cards: list[CardSet] = []
    cardsphereSetId: Optional[int] = None
    code: str
    codeV3: Optional[str] = None
    decks: list[DeckSet] = []
    isForeignOnly: Optional[bool] = None
    isFoilOnly: bool
    isNonFoilOnly: Optional[bool] = None
    isOnlineOnly: bool
    isPaperOnly: Optional[bool] = None
    isPartialPreview: Optional[bool] = None
    keyruneCode: str
    languages: Optional[list[str]] = None
    mcmId: Optional[int] = None
    mcmIdExtras: Optional[int] = None
    mcmName: Optional[str] = None
    mtgoCode: Optional[str] = None
    name: str
    parentCode: Optional[str] = None
    releaseDate: str
    sealedProduct: list[SealedProduct] = []
    tcgplayerGroupId: Optional[int] = None
    tokens: list[CardToken] = []
    tokenSetCode: Optional[str] = None
    totalSetSize: int
    translations: Translations
    type: str
