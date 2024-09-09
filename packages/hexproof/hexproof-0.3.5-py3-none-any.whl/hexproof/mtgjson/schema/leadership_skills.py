"""
* MTGJSON Schema: Leadership Skills
* https://mtgjson.com/data-models/leadership-skills/
"""
# Third Party Imports
from omnitils.schema import Schema


class LeadershipSkills(Schema):
    """Model describing the properties of formats that a card is legal to be your Commander in
        play formats that utilize Commanders."""
    brawl: bool
    commander: bool
    oathbreaker: bool
