"""
* CLI Commands: Test
"""
# Standard Library Imports
import os
import sys
from pathlib import Path

# Third Party Imports
import click
from omnitils.files import load_data_file, DisposableDir
from omnitils.logs import logger, LogResults

# Local Imports
from hexproof.mtgjson import fetch as MTGJsonFetch
from hexproof.mtgjson import schema as MTGJson
from hexproof.scryfall import fetch as ScryfallFetch
from hexproof.scryfall import schema as Scryfall
from hexproof.vectors import fetch as VectorsFetch
from hexproof.vectors import schema as Vectors

# Core variables
project_cwd = Path(__file__).parent.parent.parent

"""
* Common Parameters
"""

OPTION_trace = click.option(
    '-T', '--trace', is_flag=True, default=False,
    help='Log the traceback of any exceptions encountered.')

"""
* Commands: MTGJSON
"""


@click.command(help="Test MTGJSON 'Card' object schema.")
@OPTION_trace
def test_mtgjson_schema_card(trace: bool = False) -> None:
    """Tests MTGJSON schemas defined in `mtgjson.schema.card` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    with LogResults(
        on_failure='Invalid Schemas: Card',
        on_success='Schemas Validated: Card',
        reraise=True, log_trace=trace
    ):
        obj_atomic = MTGJsonFetch.get_cards_atomic_all()
        assert isinstance(next(iter(obj_atomic.values())), MTGJson.CardAtomic)


@click.command(help="Test MTGJSON 'CardTypes' object schema.")
@OPTION_trace
def test_mtgjson_schema_card_types(trace: bool = False) -> None:
    """Tests MTGJSON schemas defined in `mtgjson.schema.card_types` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = MTGJson.CardTypes
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        _OBJ = MTGJsonFetch.get_card_types()
        assert isinstance(_OBJ, _SCHEMA)


@click.command(help="Test MTGJSON 'Deck' object schema.")
@OPTION_trace
def test_mtgjson_schema_deck(trace: bool = False) -> None:
    """Tests MTGJSON schemas defined in `mtgjson.schema.deck` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = MTGJson.Deck
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):

        # Check all deck files
        with DisposableDir(path=project_cwd) as _path:
            all_decks = MTGJsonFetch.cache_decks_all(_path)
            for _deck in os.listdir(all_decks):
                _deck_json = all_decks / _deck

                # Check deck JSON data file
                if _deck_json.is_file() and _deck_json.suffix == '.json':
                    _OBJ = _SCHEMA(**load_data_file(_deck_json)['data'])
                    assert isinstance(_OBJ, _SCHEMA)
                    del _OBJ


@click.command(help="Test MTGJSON 'DeckList' object schema.")
@OPTION_trace
def test_mtgjson_schema_deck_list(trace: bool = False) -> None:
    """Tests MTGJSON schemas defined in `mtgjson.schema.deck_list` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = MTGJson.DeckList
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        for _OBJ in MTGJsonFetch.get_deck_list():
            assert isinstance(_OBJ, _SCHEMA)


@click.command(help="Test MTGJSON 'Keywords' object schema.")
@OPTION_trace
def test_mtgjson_schema_keywords(trace: bool = False) -> None:
    """Tests MTGJSON schemas defined in `mtgjson.schema.keywords` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = MTGJson.Keywords
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        _OBJ = MTGJsonFetch.get_keywords()
        assert isinstance(_OBJ, _SCHEMA)


@click.command(help="Test MTGJSON 'Meta' object schema.")
@OPTION_trace
def test_mtgjson_schema_meta(trace: bool = False) -> None:
    """Tests MTGJSON schemas defined in `mtgjson.schema.meta` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = MTGJson.Meta
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        _OBJ = MTGJsonFetch.get_meta()
        assert isinstance(_OBJ, _SCHEMA)


@click.command(help="Test MTGJSON 'PriceFormats' object schema.")
@OPTION_trace
def test_mtgjson_schema_price(trace: bool = False) -> None:
    """Tests MTGJSON schemas defined in `mtgjson.schema.price` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = MTGJson.PriceFormats
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        for _OBJ in MTGJsonFetch.get_prices_today_all().values():
            assert isinstance(_OBJ, _SCHEMA)


@click.command(help="Test MTGJSON 'Set' object schema.")
@OPTION_trace
def test_mtgjson_schema_set(trace: bool = False) -> None:
    """Tests MTGJSON schemas defined in `mtgjson.schema.set` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = MTGJson.Set
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):

        # Check all deck files
        with DisposableDir(path=project_cwd) as _path:
            for _FILE in MTGJsonFetch.cache_sets_all(_path).iterdir():
                if not _FILE.is_file() or _FILE.suffix != '.json':
                    continue
                _OBJ = _SCHEMA(**load_data_file(_FILE)['data'])
                assert isinstance(_OBJ, _SCHEMA)
                del _OBJ


@click.command(help="Test MTGJSON 'SetList' object schema.")
@OPTION_trace
def test_mtgjson_schema_set_list(trace: bool = False) -> None:
    """Tests MTGJSON schemas defined in `mtgjson.schema.set_list` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = MTGJson.SetList
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        for _OBJ in MTGJsonFetch.get_set_list():
            assert isinstance(_OBJ, _SCHEMA)


@click.command(
    help="Test all MTGJSON schemas.",
    context_settings={'ignore_unknown_options': True}
)
@click.pass_context
@OPTION_trace
def test_mtgjson_schema_all(ctx: click.Context, trace: bool = False) -> None:
    """Tests all MTGJSON schemas.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    logger.info('Testing Schemas: MTGJSON')
    tests = [
        test_mtgjson_schema_card_types,
        test_mtgjson_schema_deck,
        test_mtgjson_schema_deck_list,
        test_mtgjson_schema_keywords,
        test_mtgjson_schema_meta,
        test_mtgjson_schema_price,
        test_mtgjson_schema_set,
        test_mtgjson_schema_set_list
    ]

    # Test each schema
    error_encountered = False
    for func in tests:
        try:
            ctx.invoke(func, trace=trace)
        except (Exception, AssertionError):
            error_encountered = True
    if error_encountered:
        raise OSError('One or more tests failed!')


"""
* Commands: Scryfall
"""


@click.command(help="Test Scryfall 'Card' object schema.")
@OPTION_trace
def test_scryfall_schema_card(trace: bool = False) -> None:
    """Tests Scryfall schemas defined in `scryfall.schema.card` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = Scryfall.Card
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        _OBJ = ScryfallFetch.get_card_named('Damnation', set_code='TSR')
        assert isinstance(_OBJ, _SCHEMA)


@click.command(help="Test Scryfall 'Ruling' object schema.")
@OPTION_trace
def test_scryfall_schema_ruling(trace: bool = False) -> None:
    """Tests Scryfall schemas defined in `scryfall.schema.ruling` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = Scryfall.Ruling
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        for _OBJ in ScryfallFetch.get_card_rulings('CMA', '176'):
            assert isinstance(_OBJ, _SCHEMA)


@click.command(help="Test Scryfall 'Set' object schema.")
@OPTION_trace
def test_scryfall_schema_set(trace: bool = False) -> None:
    """Tests Scryfall schemas defined in `scryfall.schema.set` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = Scryfall.Set
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        for _OBJ in ScryfallFetch.get_set_list():
            assert isinstance(_OBJ, _SCHEMA)


@click.command(
    help="Test all Scryfall schemas.",
    context_settings={'ignore_unknown_options': True})
@click.pass_context
@OPTION_trace
def test_scryfall_schema_all(ctx: click.Context, trace: bool = False) -> None:
    """Tests all Scryfall schemas.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    logger.info('Testing Schemas: Scryfall')
    tests = [
        test_scryfall_schema_card,
        test_scryfall_schema_ruling,
        test_scryfall_schema_set
    ]

    # Test each schema
    error_encountered = False
    for func in tests:
        try:
            ctx.invoke(func, trace=trace)
        except (OSError, Exception):
            error_encountered = True
    if error_encountered:
        raise OSError('One or more tests failed!')


"""
* Commands: MTG Vectors
"""


@click.command(help='Test MTG Vectors release schema.')
@OPTION_trace
def test_vectors_schema_release(trace: bool = False) -> None:
    """Tests MTG Vectors 'Manifest' schema and nested schemas defined in `vectors.schema` module.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    _SCHEMA = Vectors.Meta
    with LogResults(
        on_failure=f'Invalid Schemas: {_SCHEMA.__name__}',
        on_success=f'Schemas Validated: {_SCHEMA.__name__}',
        reraise=True, log_trace=trace
    ):
        for _OBJ in VectorsFetch.get_latest_release().values():
            assert isinstance(_OBJ, _SCHEMA)


@click.command(
    help='Test all MTG Vectors schemas.',
    context_settings={'ignore_unknown_options': True})
@click.pass_context
@OPTION_trace
def test_vectors_schema_all(ctx: click.Context, trace: bool = False) -> None:
    """Tests all MTG Vectors schemas.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    logger.info('Testing Schemas: MTG Vectors')
    tests = [
        test_vectors_schema_release,
    ]

    # Test each schema
    error_encountered = False
    for func in tests:
        try:
            ctx.invoke(func, trace=trace)
        except (OSError, Exception):
            error_encountered = True
    if error_encountered:
        raise OSError


"""
* Generic Commands
"""


@click.command(
    help="Test all schemas.",
    context_settings={'ignore_unknown_options': True})
@click.pass_context
@OPTION_trace
def test_all_schemas(ctx: click.Context, trace: bool = False) -> None:
    """Tests every schema group.

    Args:
        trace: Whether to log the traceback of any exceptions encountered.
    """
    tests = [
        test_mtgjson_schema_all,
        test_scryfall_schema_all,
        test_vectors_schema_all
    ]

    # Test each schema
    error_encountered = False
    for func in tests:
        try:
            ctx.invoke(func, trace=trace)
        except OSError:
            error_encountered = True
    if error_encountered:
        raise OSError


"""
* Command Groups
"""


class TestSchema(click.Group):
    def __init__(self, *_args, **_kwargs) -> None:
        super().__init__(
            name='test-schema',
            commands={
                '.': test_all_schemas,
                'mtgjson': TestMTGJSONSchema(),
                'scryfall': TestScryfallSchema(),
                'vectors': TestVectorsSchema()
            },
            help="A command group for testing hexproof module schemas.",
            context_settings={'ignore_unknown_options': True},
            invoke_without_command=True
        )

    def invoke(self, ctx: click.Context):
        try:
            if not ctx.protected_args and '--help' not in ctx.args:
                return ctx.invoke(self.get_command(ctx, '.'))
            return super().invoke(ctx)
        except click.ClickException:
            logger.exception('Encountered a Click CLI exception!')
            sys.exit(1)
        except (OSError, Exception):
            logger.error('One or more tests failed!', show_location=False)
            sys.exit(1)


class TestMTGJSONSchema(click.Group):
    def __init__(self, *_args, **_kwargs) -> None:
        super().__init__(
            name='mtgjson',
            commands={
                '.': test_mtgjson_schema_all,
                'card-types': test_mtgjson_schema_card_types,
                'deck': test_mtgjson_schema_deck,
                'deck-list': test_mtgjson_schema_deck_list,
                'keywords': test_mtgjson_schema_keywords,
                'meta': test_mtgjson_schema_meta,
                'price': test_mtgjson_schema_price,
                'set': test_mtgjson_schema_set,
                'set-list': test_mtgjson_schema_set_list,
            },
            help="A command group for performing MTGJSON schema tests.",
            context_settings={'ignore_unknown_options': True},
            invoke_without_command=True
        )

    def invoke(self, ctx: click.Context) -> None:
        if ctx.invoked_subcommand is None and '--help' not in ctx.args:
            return ctx.invoke(self.get_command(ctx, '.'))
        return super().invoke(ctx)


class TestScryfallSchema(click.Group):
    def __init__(self, *_args, **_kwargs) -> None:
        super().__init__(
            name='scryfall',
            commands={
                '.': test_scryfall_schema_all,
                'card': test_scryfall_schema_card,
                'ruling': test_scryfall_schema_ruling,
                'set': test_scryfall_schema_set
            },
            help="A command group for performing Scryfall schema tests.",
            context_settings={'ignore_unknown_options': True},
            invoke_without_command=True
        )

    def invoke(self, ctx: click.Context) -> None:
        if not ctx.protected_args and '--help' not in ctx.args:
            return ctx.invoke(self.get_command(ctx, '.'))
        return super().invoke(ctx)


class TestVectorsSchema(click.Group):
    """Command group for performing MTG Vectors schema tests."""
    def __init__(self, *_args, **_kwargs) -> None:
        super().__init__(
            name='vectors',
            commands={
                '.': test_vectors_schema_all,
                'release': test_vectors_schema_release
            },
            help="A command group for performing MTG Vectors schema tests.",
            context_settings={'ignore_unknown_options': True},
            invoke_without_command=True
        )

    def invoke(self, ctx: click.Context) -> None:
        if not ctx.protected_args and '--help' not in ctx.args:
            return ctx.invoke(self.get_command(ctx, '.'))
        return super().invoke(ctx)
