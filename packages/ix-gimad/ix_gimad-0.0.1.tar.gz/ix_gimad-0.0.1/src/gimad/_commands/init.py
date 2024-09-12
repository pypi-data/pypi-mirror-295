import shutil
from pathlib import Path
from typing import Annotated

from rich import print
from typer import Argument, Option

from gimad._config import Config
from gimad._utils import CONFIG_NAME, ONEOFF_DIR_NAME, PERMANENT_DIR_NAME


def _create_config() -> None:
    config = Config(db_url="postgresql://user:password@host:port/database")
    config_path = Path(f"{CONFIG_NAME}.json")
    config_path.write_text(config.model_dump_json(indent=2))


def init(
    migration_dir: Annotated[
        str,
        Argument(help="Name of the directory to store migration scripts"),
    ] = "data_migrations",
    force: Annotated[
        bool,
        Option(
            "--force",
            "-f",
            help="Force initialization, can cause data loss if there are files in the related directories",
        ),
    ] = False,
) -> None:
    """Initialize current directory with data migration directory structure"""
    migration_root = Path(migration_dir)
    if force:
        shutil.rmtree(migration_root)
    migration_root.mkdir()
    for d in (PERMANENT_DIR_NAME, ONEOFF_DIR_NAME):
        migration_root.joinpath(d).mkdir()
    _create_config()
    print("[green]Gimad successfully initialized[/green]")
