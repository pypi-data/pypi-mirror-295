import contextlib
from collections.abc import Sequence
from typing import Self

import psycopg
from psycopg.errors import DuplicateTable


class DatabaseClient:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url

    def __enter__(self) -> Self:
        self._connection = psycopg.connect(self.db_url, autocommit=True)
        self._cursor = self._connection.cursor()
        return self

    def __exit__(self, type: object, value: object, traceback: object) -> None:
        self._cursor.close()
        self._connection.close()

    def setup_history_table(self) -> None:
        with contextlib.suppress(DuplicateTable):
            self._cursor.execute(
                """
                create table data_migrations(
                    name varchar primary key,
                    type varchar not null,
                    created_at timestamptz not null default now()
                )
                """,
            )

    def exclude_executed_scripts(self, scripts: Sequence[str]) -> list:
        res = self._cursor.execute(
            """
            with all_scripts as (
                select unnest((%s)::varchar[]) name
                )
            select name
            from all_scripts
            where all_scripts.name not in (select name from data_migrations)
            """,
            [scripts],
        )
        return [r[0] for r in res]

    def query_last_executed_migrations(self, n: int) -> list[dict[str, str]]:
        rows = self._cursor.execute(
            """
            select name, type
            from data_migrations
            order by name desc
            limit %s
            """,
            [n],
        )
        return [{"name": r[0], "type": r[1]} for r in rows]

    def mark_executed(self, name: str, type: str) -> None:
        self._cursor.execute(
            """
            insert into data_migrations(name, type)
            values(%s, %s)
            """,
            [name, type],
        )

    def unmark_executed(self, name: str, type: str) -> None:
        self._cursor.execute(
            """
            delete from data_migrations
            where name = %s and type = %s
            """,
            [name, type],
        )
