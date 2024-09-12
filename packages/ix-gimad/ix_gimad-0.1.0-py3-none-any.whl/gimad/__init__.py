import os

from typer import Typer

from gimad._commands.down import down
from gimad._commands.init import init
from gimad._commands.new import new
from gimad._commands.redo import redo
from gimad._commands.up import up
from gimad._utils import error

app = Typer(
    no_args_is_help=True,
    help="""
Non-schema migration runner for PostgreSQL

For debugging, set the environment variable DEBUG=1 to see the stack trace
    """,
)
init = app.command()(init)
new = app.command()(new)
up = app.command()(up)
down = app.command()(down)
redo = app.command()(redo)


def main() -> None:
    try:
        app()
    except Exception as e:  # noqa: BLE001
        if not os.environ.get("DEBUG"):
            error(str(e))
        else:
            raise
