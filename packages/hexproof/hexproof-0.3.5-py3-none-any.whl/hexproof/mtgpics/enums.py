"""
* MTGPics Enums
"""
# Standard Libray Imports
from dataclasses import dataclass

# Third Party Imports
import yarl

# Core variables
__MTGPICS_ROOT__ = yarl.URL('https://mtgpics.com')

"""
* URL Enums
"""


@dataclass
class MTGPicsURL:
    """MTGPics page URLs."""
    Main = __MTGPICS_ROOT__
    Art = Main / 'art'
    Card = Main / 'card'
    Illus = Main / 'illus'
    IllusList = Main / 'illus_txt'
    Illustrators = Main / 'illustrators'
    Pics = Main / 'pics'
    PicsArt = Main / 'art'
    PicsArtThumb = Pics / 'art_th'
    PicsBig = Pics / 'big'
    PicsReg = Pics / 'reg'
    Set = Main / 'set'
    SetChecklist = Main / 'set_checklist'
    Sets = Main / 'sets'
    SetsChrono = Main / 'sets_chrono'
    SetsSoon = Main / 'sets_soon'
    Spoiler = Main / 'spoiler'
