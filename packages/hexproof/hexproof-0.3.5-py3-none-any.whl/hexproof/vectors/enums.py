"""
* MTG Vectors Enums
"""
# Standard Library Imports
from dataclasses import dataclass

# Third Party Imports
from omnitils.enums import StrConstant

# Third Party Imports
import yarl

"""
* Enums
"""


@dataclass
class VectorURL:
    API = yarl.URL('https://api.github.com')
    DefaultReleases = API / 'repos/Investigamer/mtg-vectors/releases/latest'
    DefaultPackages = yarl.URL('https://github.com/Investigamer/mtg-vectors/releases/download')


class SymbolRarity(StrConstant):
    EIGHTY = '80'
    B = 'B'
    C = 'C'
    H = 'H'
    M = 'M'
    R = 'R'
    S = 'S'
    T = 'T'
    U = 'U'
    WM = 'WM'


RarityNameMap: dict[str, SymbolRarity] = {
    'EIGHTY': SymbolRarity.EIGHTY,
    'BONUS': SymbolRarity.B,
    'COMMON': SymbolRarity.C,
    'HALF': SymbolRarity.H,
    'MYTHIC': SymbolRarity.M,
    'RARE': SymbolRarity.R,
    'SPECIAL': SymbolRarity.S,
    'TIMESHIFTED': SymbolRarity.T,
    'UNCOMMON': SymbolRarity.U,
    'WATERMARK': SymbolRarity.WM,
}
