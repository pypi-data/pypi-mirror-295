"""
* MTGJSON Schema: Set List
* https://mtgjson.com/data-models/set-list/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema

# Local Imports
from hexproof.mtgjson.schema.sealed_product import SealedProduct
from hexproof.mtgjson.schema.translations import Translations


class SetList(Schema):
    """Model describing the meta data properties of an individual Set."""
    baseSetSize: int
    block: Optional[str] = None
    code: str
    codeV3: Optional[str] = None
    isForeignOnly: Optional[bool] = None
    isFoilOnly: bool = False
    isNonFoilOnly: Optional[bool] = None
    isOnlineOnly: bool = False
    isPaperOnly: Optional[bool] = None
    isPartialPreview: Optional[bool] = None
    keyruneCode: str
    mcmId: Optional[int] = None
    mcmIdExtras: Optional[int] = None
    mcmName: Optional[str] = None
    mtgoCode: Optional[str] = None
    name: str
    parentCode: Optional[str] = None
    releaseDate: str
    sealedProduct: list[SealedProduct] = []
    tcgplayerGroupId: Optional[int] = None
    totalSetSize: int
    translations: Translations
    type: str
