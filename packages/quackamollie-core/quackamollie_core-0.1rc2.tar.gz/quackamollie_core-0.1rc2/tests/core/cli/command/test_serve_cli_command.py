# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from click.testing import CliRunner, Result

from quackamollie.core.quackamollie import quackamollie


def test_quackamollie_serve_help():
    """ Testing Quackamollie serve command integration by calling `quackamollie serve -h/--help`

        Arrange/Act: Run the help of the command `quackamollie serve` to verify its import.
        Assert: The output contains the description of the serve command
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(quackamollie, ['serve', '-h'])
    print(f"result.output.strip()={result.output.strip()}")
    assert "CLI command to serve Quackamollie bot which polls and answers Telegram" in result.output.strip(), \
        "'serve' command helper should have been printed."
