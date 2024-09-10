# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from click.testing import CliRunner, Result

from quackamollie.core import core_version
from quackamollie.core.quackamollie import quackamollie


def test_version_displays_library_version():
    """ Test `quackamollie --version` option

        Arrange/Act: Run the `--version` option.
        Assert: The output matches the library version.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(quackamollie, ['--version'])
    assert core_version in result.output.strip(), 'Version number should match library version.'


def test_quackamollie_help():
    """ Testing Quackamollie groups integration by calling `quackamollie -h/--help`

        Arrange/Act: Run the help of the group `quackamollie` to verify its import.
        Assert: The output contains a list of quackamollie subgroups.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(quackamollie, ['-h'])
    print(f"result.output.strip()={result.output.strip()}")
    assert "db     CLI group to handle database's URL" in result.output.strip(), "'db' subgroup should be listed."
    assert "serve  CLI command to serve Quackamollie" in result.output.strip(), "'serve' subgroup should be listed."
