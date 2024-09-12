from typing import Annotated, Optional

from typer import Option

from gimad._config import load_config
from gimad._db import DatabaseClient
from gimad._runner import Runner


def up(
    count: Annotated[
        # Typer limitation. See https://github.com/tiangolo/typer/pull/739
        Optional[int],  # noqa: UP007
        Option("-c", "--count", help="Number of migrations to run"),
    ] = None,
    skip_oneoff: Annotated[
        bool,
        Option(
            help="""
Only run permanent migrations

This option is useful for initializing a new database.
            """,
        ),
    ] = False,
) -> None:
    """Run pending migrations"""
    config = load_config()
    with DatabaseClient(config.db_url) as client:
        Runner(client).up(count, skip_oneoff)
