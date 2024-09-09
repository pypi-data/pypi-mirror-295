"""
* MTGJSON Schema: Translations
* https://mtgjson.com/data-models/translations/
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.schema import Schema
from pydantic import Field


class Translations(Schema):
    """Model describing the properties of a Set or Set List's name translated in various alternate languages."""
    Ancient_Greek: Optional[str] = Field(None, alias="Ancient Greek")
    Arabic: Optional[str] = Field(None, alias="Arabic")
    Chinese_Simplified: Optional[str] = Field(None, alias="Chinese Simplified")
    Chinese_Traditional: Optional[str] = Field(None, alias="Chinese Traditional")
    French: Optional[str] = Field(None, alias="French")
    German: Optional[str] = Field(None, alias="German")
    Hebrew: Optional[str] = Field(None, alias="Hebrew")
    Italian: Optional[str] = Field(None, alias="Italian")
    Japanese: Optional[str] = Field(None, alias="Japanese")
    Korean: Optional[str] = Field(None, alias="Korean")
    Latin: Optional[str] = Field(None, alias="Latin")
    Phyrexian: Optional[str] = Field(None, alias="Phyrexian")
    Portuguese_Brazil: Optional[str] = Field(None, alias="Portuguese (Brazil)")
    Russian: Optional[str] = Field(None, alias="Russian")
    Sanskrit: Optional[str] = Field(None, alias="Sanskrit")
    Spanish: Optional[str] = Field(None, alias="Spanish")
