# -*- coding: utf-8 -*-
__all__ = ["db"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import click
import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import Optional

from quackamollie.core.cli.helpers.db_url_config import get_db_url_from_config, anonymize_database_url
from quackamollie.core.cli.helpers.entry_point_command import get_commands_from_entry_points
from quackamollie.core.cli.settings import QuackamollieSettings, pass_quackamollie_settings
from quackamollie.core.defaults import DEFAULT_DB_PROTOCOL, DEFAULT_DB_HOST, DEFAULT_DB_NAME

log = logging.getLogger(__name__)


@click.group(context_settings={'auto_envvar_prefix': 'QUACKAMOLLIE'},
             commands=get_commands_from_entry_points('quackamollie.command.db'))
@click.help_option('-h', '--help')
@click.option('-dbpr', '--db-protocol', type=str, default=DEFAULT_DB_PROTOCOL,
              show_default=True, help="Database protocol, must be a protocol supported by SQLAlchemy")
@click.option('-dbu', '--db-username', type=str, default=None, show_default=True,
              help="Username for postgres database connection")
@click.option('-dbpa', '--db-password', type=str, default=None, show_default=False,
              help="Password for postgres database connection")
@click.option('-dbh', '--db-host', type=str, default=DEFAULT_DB_HOST, show_default=True,
              help="Hostname of the postgres database")
@click.option('-dbpo', '--db-port', type=int, default=None, show_default=True,
              help="Port of the postgres database")
@click.option('-dbn', '--db-name', type=str, default=DEFAULT_DB_NAME, show_default=True,
              help="Name of the postgres database")
@click.option('--db-url', type=str, default=None, show_default=True,
              help="Override of the URL of the postgres database, by default it is inferred from '--db-*' options")
@pass_quackamollie_settings
@click.pass_context
def db(ctx, settings: QuackamollieSettings, db_protocol: str, db_username: Optional[str], db_password: Optional[str],
       db_host: str, db_port: Optional[int], db_name: str, db_url: Optional[str]):
    """ CLI group to handle database's URL configuration and call associated database commands.\f

        :param ctx: Click context to pass between commands of quackamollie
        :type ctx: click.Context

        :param settings: Quackamollie settings to pass between commands of quackamollie
        :type settings: QuackamollieSettings

        :param db_protocol: Database protocol, must be a protocol supported by SQLAlchemy
        :type db_protocol: str

        :param db_username: Username for postgres database connection
        :type db_username: Optional[str]

        :param db_password: Password for postgres database connection
        :type db_password: Optional[str]

        :param db_host: Hostname of the postgres database
        :type db_host: str

        :param db_port: Port of the postgres database
        :type db_port: Optional[str]

        :param db_name: Name of the postgres database
        :type db_name: str

        :param db_url: Override of the URL of the postgres database, by default it is inferred from '--db-*' options
        :type db_url: Optional[str]
    """
    # Add new configurations to context
    settings.db_protocol = db_protocol
    settings.db_username = db_username
    settings.db_password = db_password
    settings.db_host = db_host
    settings.db_port = db_port
    settings.db_name = db_name

    # Set inferred database URL
    if db_url is None:
        settings.db_url = get_db_url_from_config(db_protocol, db_host, db_name, db_username=db_username,
                                                 db_password=db_password, db_port=db_port)
        db_url_parameter_source = "INFERRED"
    else:
        settings.db_url = db_url
        db_url_parameter_source = ctx.get_parameter_source('db_url').name
    settings.anonymized_db_url = anonymize_database_url(settings.db_url)

    # Log configuration for debug, with username partially hidden and password fully hidden
    log.debug(f"Database input settings are :"
              f"\n\tdb_protocol: {settings.db_protocol} [from {ctx.get_parameter_source('db_protocol').name}]"
              f"\n\tdb_username: {settings.anonymized_db_username}"
              f" [from {ctx.get_parameter_source('db_username').name}]"
              f"\n\tdb_password: {settings.anonymized_db_password}"
              f" [from {ctx.get_parameter_source('db_password').name}]"
              f"\n\tdb_host: {settings.db_host} [from {ctx.get_parameter_source('db_host').name}]"
              f"\n\tdb_port: {settings.db_port} [from {ctx.get_parameter_source('db_port').name}]"
              f"\n\tdb_name: {settings.db_name} [from {ctx.get_parameter_source('db_name').name}]"
              f"\n\tdb_url: {settings.anonymized_db_url} [from {db_url_parameter_source}]")

    # Initialize database connectors
    # cf. SQLAlchemy 2.0 documentation: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm
    settings.engine = create_async_engine(settings.db_url, echo=True)
    settings.session = async_sessionmaker(settings.engine, expire_on_commit=False)

    # Disable settings edition before launching asynchronous processing
    settings.enable_settings_edition = False
