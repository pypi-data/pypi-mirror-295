"""
* CLI Application
* Primarily used for testing and development.
"""
# Third Party Imports
import click

# Local Imports
from .test_schema import TestSchema


class MainCLIGroup(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, commands={'test-schema': TestSchema()}, **kwargs)


# Export CLI Application
HexproofCLI = MainCLIGroup()
__all__ = ['HexproofCLI']
