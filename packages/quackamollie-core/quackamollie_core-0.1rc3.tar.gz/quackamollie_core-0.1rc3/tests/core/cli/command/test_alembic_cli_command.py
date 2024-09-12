# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from click.testing import CliRunner, Result

from quackamollie.core.quackamollie import quackamollie


def test_quackamollie_db_alembic_help():
    """ Testing Quackamollie alembic command integration by calling `quackamollie db alembic -h/--help`

        Arrange/Act: Run the help of the command `quackamollie db alembic` to verify its import.
        Assert: The output contains some fields specific to the alembic CLI, which proves this CLI can be called through
                the quackamollie click CLI
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(quackamollie, ['db', 'alembic', '-h'])
    print(f"result.output.strip()={result.output.strip()}")
    assert "current             Display the current revision for a database." in result.output.strip(), \
        "'current' alembic command helper should have been printed."
