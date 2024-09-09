"""
* MTGJSON Schema: Identifiers
* https://mtgjson.com/data-models/identifiers/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema


class Identifiers(Schema):
    """Model describing the properties of identifiers associated to a card."""
    cardKingdomEtchedId: Optional[str] = None
    cardKingdomFoilId: Optional[str] = None
    cardKingdomId: Optional[str] = None
    cardsphereId: Optional[str] = None
    mcmId: Optional[str] = None
    mcmMetaId: Optional[str] = None
    mtgArenaId: Optional[str] = None
    mtgjsonFoilVersionId: Optional[str] = None
    mtgjsonNonFoilVersionId: Optional[str] = None
    mtgjsonV4Id: Optional[str] = None
    mtgoFoilId: Optional[str] = None
    mtgoId: Optional[str] = None
    multiverseId: Optional[str] = None
    scryfallId: Optional[str] = None
    scryfallOracleId: Optional[str] = None
    scryfallIllustrationId: Optional[str] = None
    tcgplayerProductId: Optional[str] = None
    tcgplayerEtchedProductId: Optional[str] = None
