import sys
from enum import StrEnum, auto
from importlib import import_module
from pathlib import Path
from typing import Protocol, Self

from pydantic import BaseModel, ConfigDict
from rich import print

from gimad._db import DatabaseClient
from gimad._utils import ONEOFF_DIR, PERMANENT_DIR


class MigrationError(Exception):
    """General migration error"""


class MigrationType(StrEnum):
    PERMANENT = auto()
    ONEOFF = auto()


class MigrationModule(Protocol):
    def up(self) -> None: ...
    def down(self) -> None: ...


class Migration(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str
    type: MigrationType

    @classmethod
    def from_path(cls, p: Path) -> Self:
        return cls.model_validate({"name": p.name, "type": p.parent.name})

    @property
    def module(self) -> MigrationModule:
        m = import_module(self.name.removesuffix(".py"))
        for func in ["up", "down"]:
            if not hasattr(m, func):
                msg = f"Migration file {self.type}/{self.name} missing `{func}()` function"
                raise MigrationError(msg)
        return m  # type: ignore


def _append_paths() -> None:
    sys.path.append(str(ONEOFF_DIR.resolve()))
    sys.path.append(str(PERMANENT_DIR.resolve()))


def _collect_migrations(skip_oneoff: bool = False) -> list[Migration]:
    """Collect all migration scripts from migration script directory"""
    scripts = [Migration.from_path(p) for p in PERMANENT_DIR.glob("*.py")]
    if not skip_oneoff:
        oneoff_scripts = ONEOFF_DIR.glob("*.py")
        scripts.extend(Migration.from_path(p) for p in oneoff_scripts)
    return scripts


class Runner:
    """Migration runner"""

    def __init__(self, client: DatabaseClient) -> None:
        _append_paths()
        self._client = client
        self._client.setup_history_table()

    def up(self, n: int | None = None, skip_oneoff: bool = False) -> None:
        """
        Run the upgrade code path of all pending migrations

        If `n` is specfied, only run the first `n` migrations.
        """
        self._migrations = self._collect_pending_migrations(skip_oneoff)
        if not self._migrations:
            print("[blue]Nothing to run[/blue]")
            return

        if n:
            self._up_with_count(n)
            return

        for migration in self._migrations:
            self._migrate(migration)

    def _up_with_count(self, n: int) -> None:
        for migration in self._migrations:
            if n < 1:
                return
            self._migrate(migration)
            n -= 1

    def down(self, n: int) -> None:
        """Run the downgrade code path of `n` latest migration"""
        self._migrations = self._collect_executed_migrations(n)
        for migration in reversed(self._migrations):
            if n < 1:
                return
            self._rollback(migration)
            n -= 1

    def _collect_pending_migrations(self, skip_oneoff: bool) -> list[Migration]:
        scripts = _collect_migrations(skip_oneoff)
        pending = set(self._client.exclude_executed_scripts([s.name for s in scripts]))
        return sorted((s for s in scripts if s.name in pending), key=lambda s: s.name)

    def _collect_executed_migrations(self, n: int) -> list[Migration]:
        rows = self._client.query_last_executed_migrations(n)
        return [Migration.model_validate(r) for r in rows]

    def _migrate(self, migration: Migration) -> None:
        print(f"[blue]:: Migrating {migration.type}/{migration.name}[/blue]")
        migration.module.up()
        self._client.mark_executed(migration.name, migration.type)

    def _rollback(self, migration: Migration) -> None:
        print(f"[blue]:: Rolling back {migration.type}/{migration.name}[/blue]")
        migration.module.down()
        self._client.unmark_executed(migration.name, migration.type)
