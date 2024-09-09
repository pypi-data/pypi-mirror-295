"""
* Hexproof API Enums
"""
# Standard Library Imports
from dataclasses import dataclass

# Third Party Imports
from yarl import URL

# Constants
__HEX_SITE__: URL = URL('https://hexproof.io')
__HEX_API__: URL = URL('https://api.hexproof.io')
__HEX_CDN__: URL = URL('https://cdn.hexproof.io')


@dataclass
class HexURL:
    """Catalogued URL hierarchy for the Hexproof API data source."""

    # Main domain
    Main: URL = __HEX_SITE__

    # CDN domain
    CDN: URL = __HEX_CDN__

    @dataclass
    class API:
        """Hexproof REST API endpoints."""
        Main: URL = __HEX_SITE__
        Docs: URL = Main / 'docs'

        @dataclass
        class Keys:
            """API endpoint for Key objects."""
            All = __HEX_API__ / 'keys'

        @dataclass
        class Meta:
            """API endpoint for Meta objects."""
            All = __HEX_API__ / 'meta'

        @dataclass
        class Sets:
            """API endpoint for Set objects."""
            All = __HEX_API__ / 'sets'

        @dataclass
        class Symbols:
            """API endpoint for Symbol objects."""
            All = __HEX_API__ / 'symbols'
            Watermark = All / 'watermark'
            Set = All / 'sets'
