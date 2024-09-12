# -*- coding: utf-8 -*-
__all__ = ["alembic"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import click

from alembic.config import main

from quackamollie.core.cli.settings import QuackamollieSettings, pass_quackamollie_settings


@click.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
               add_help_option=False)
@click.argument('alembic_args', nargs=-1, type=click.UNPROCESSED)
@pass_quackamollie_settings
@click.pass_context
def alembic(_: click.Context, __: QuackamollieSettings, alembic_args):
    """ Alembic CLI wrapper to handle database's URL configuration. Arguments are passed to alembic's main CLI.\f

        :param _: Click context to pass between commands of quackamollie
        :type _: click.Context

        :param __: Quackamollie settings to pass between commands of quackamollie
        :type __: QuackamollieSettings

        :param alembic_args: A list of additional arguments to pass to the Alembic CLI main function
        :type alembic_args: List
    """
    main(alembic_args)
