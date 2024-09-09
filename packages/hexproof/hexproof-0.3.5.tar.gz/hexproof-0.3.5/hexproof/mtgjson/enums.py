"""
* MTGJSON Enums
"""
# Standard Library Imports
from dataclasses import dataclass

# Third Party Imports
import yarl

# Constants
__MTGJSON_SITE__ = yarl.URL('https://mtgjson.com')
__MTGJSON_API__ = __MTGJSON_SITE__ / 'api' / 'v5'

"""
* URL Enums
"""


@dataclass
class MTGJsonURL:
    """Catalogued URL hierarchy for the MTGJson data source."""
    Site = __MTGJSON_SITE__
    API = __MTGJSON_API__

    """Root directories."""
    CSV = API / 'csv'
    Decks = API / 'decks'
    Parquet = API / 'parquet'
    Sets = API

    class BulkZip:
        """Bulk data file archives."""
        AllDeckFiles = __MTGJSON_API__ / 'AllDeckFiles.tar.gz'
        AllPrintingsCSVFiles = __MTGJSON_API__ / 'AllPrintingsCSVFiles.tar.gz'
        AllPrintingsParquetFiles = __MTGJSON_API__ / 'AllPrintingsParquetFiles.tar.gz'
        AllSetFiles = __MTGJSON_API__ / 'AllSetFiles.tar.gz'

    @dataclass
    class BulkJSON:
        """Bulk data files."""
        AllIdentifiers = __MTGJSON_API__ / 'AllIdentifiers.json'
        AllPrices = __MTGJSON_API__ / 'AllPrices.json'
        AllPricesToday = __MTGJSON_API__ / 'AllPricesToday.json'
        AllPrintings = __MTGJSON_API__ / 'AllPrintings.json'
        AtomicCards = __MTGJSON_API__ / 'AtomicCards.json'
        CardTypes = __MTGJSON_API__ / 'CardTypes.json'
        CompiledList = __MTGJSON_API__ / 'CompiledList.json'
        DeckList = __MTGJSON_API__ / 'DeckList.json'
        EnumValues = __MTGJSON_API__ / 'EnumValues.json'
        Keywords = __MTGJSON_API__ / 'Keywords.json'
        Legacy = __MTGJSON_API__ / 'Legacy.json'
        LegacyAtomic = __MTGJSON_API__ / 'LegacyAtomic.json'
        Meta = __MTGJSON_API__ / 'Meta.json'
        Modern = __MTGJSON_API__ / 'Modern.json'
        ModernAtomic = __MTGJSON_API__ / 'ModernAtomic.json'
        PauperAtomic = __MTGJSON_API__ / 'PauperAtomic.json'
        Pioneer = __MTGJSON_API__ / 'Pioneer.json'
        PioneerAtomic = __MTGJSON_API__ / 'PioneerAtomic.json'
        SetList = __MTGJSON_API__ / 'SetList.json'
        Standard = __MTGJSON_API__ / 'Standard.json'
        StandardAtomic = __MTGJSON_API__ / 'StandardAtomic.json'
        TcgplayerSkus = __MTGJSON_API__ / 'TcgplayerSkus.json'
        Vintage = __MTGJSON_API__ / 'Vintage.json'
        VintageAtomic = __MTGJSON_API__ / 'VintageAtomic.json'
