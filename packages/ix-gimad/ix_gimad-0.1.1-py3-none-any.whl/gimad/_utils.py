import os
import sys
from pathlib import Path

from rich import print

PERMANENT_DIR_NAME = "permanent"
ONEOFF_DIR_NAME = "oneoff"

MIGRATION_DIR = Path(os.environ.get("GIMAD_MIGRATION_DIR", "data_migrations")).resolve()
PERMANENT_DIR = MIGRATION_DIR.joinpath(PERMANENT_DIR_NAME)
ONEOFF_DIR = MIGRATION_DIR.joinpath(ONEOFF_DIR_NAME)

CONFIG_NAME = "gimad"


def error(message: str) -> None:
    print(f"[red]ERROR: {message}[/red]", file=sys.stderr)
