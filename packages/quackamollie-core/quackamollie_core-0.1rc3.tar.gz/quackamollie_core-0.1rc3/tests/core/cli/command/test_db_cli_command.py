# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from click.testing import CliRunner, Result

from quackamollie.core.quackamollie import quackamollie


def test_quackamollie_db_help():
    """ Testing Quackamollie db group integration by calling `quackamollie db -h/--help`

        Arrange/Act: Run the help of the group `quackamollie db` to verify its import.
        Assert: The output contains a description of the db group, and lists also quackamollie db's subcommands.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(quackamollie, ['db', '-h'])
    print(f"result.output.strip()={result.output.strip()}")
    assert "CLI group to handle database's URL configuration and call associated database" in result.output.strip(), \
        "'db' group helper should have been printed."
    assert "alembic  Alembic CLI wrapper to handle database's" in result.output.strip(), \
        "'alembic' subcommand should have been listed."
