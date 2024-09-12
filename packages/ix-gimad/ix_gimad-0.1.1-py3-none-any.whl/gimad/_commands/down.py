from typing import Annotated

from typer import Option

from gimad._config import load_config
from gimad._db import DatabaseClient
from gimad._runner import Runner


def down(
    count: Annotated[
        int,
        Option("-c", "--count", help="Number of migrations to rollback", min=1),
    ] = 1,
) -> None:
    """Run rollback scripts"""
    config = load_config()
    with DatabaseClient(config.db_url) as client:
        Runner(client).down(count)
