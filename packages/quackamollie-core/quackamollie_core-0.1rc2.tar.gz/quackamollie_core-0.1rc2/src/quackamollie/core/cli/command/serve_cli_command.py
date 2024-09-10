# -*- coding: utf-8 -*-
__all__ = ["parse_ids_list", "serve"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import asyncio
import click
import logging
import os

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import List, Optional

from quackamollie.core.bot.quackamollie_bot import get_commands_list, start_quackamollie_bot
from quackamollie.core.cli.helpers.db_url_config import get_db_url_from_config, anonymize_database_url
from quackamollie.core.cli.settings import QuackamollieSettings, pass_quackamollie_settings
from quackamollie.core.defaults import (DEFAULT_OLLAMA_BASE_URL, DEFAULT_MODEL_MANAGER, DEFAULT_MODEL,
                                        DEFAULT_DATA_DIR, DEFAULT_DB_PROTOCOL, DEFAULT_DB_HOST, DEFAULT_DB_NAME,
                                        DEFAULT_HISTORY_MAX_LENGTH, DEFAULT_MIN_NB_CHUNK_TO_SHOW)
from quackamollie.core.model_manager_registry.model_manager_registry import QuackamollieModelManagerRegistry

log = logging.getLogger(__name__)


def parse_ids_list(_: click.Context, param, value: str) -> List[int]:
    """ Parse option string to list of integer ids

        :param _: The current click context
        :type _: click.Context

        :param param: The currently parsed parameter

        :param value: A string containing a list of comma separated integer values
        :type value: str

        :return: A list of integer ids
        :rtype: List[int]
    """
    try:
        return list(map(int, value.split(","))) if value else []
    except (ValueError, TypeError):
        raise click.BadParameter(f"Value format should be positive integers separated by commas but '{value}'"
                                 f" doesn't match this format.", param_hint=" / ".join([f"'{p}'" for p in param.opts]))


@click.command(context_settings={'auto_envvar_prefix': 'QUACKAMOLLIE'})
@click.help_option('-h', '--help')
@click.option('-t', '--bot-token', type=str, required=True, help="Telegram bot API token")
@click.option('-a', '--admin-ids', type=str, default=None, show_default=True, callback=parse_ids_list,
              help="A list of admin user ids separated by commas")
@click.option('-m', '--moderator-ids', type=str, default=None, show_default=True, callback=parse_ids_list,
              help="A list of moderator user ids separated by commas")
@click.option('-u', '--user-ids', type=str, default=None, show_default=True, callback=parse_ids_list,
              help="A list of user ids separated by commas")
@click.option('-d', '--data-dir', type=click.Path(exists=False, file_okay=False), default=DEFAULT_DATA_DIR,
              show_default=True, help="Data directory dedicated to Quackamollie's data")
@click.option('-o', '--ollama-base-url', type=str, default=DEFAULT_OLLAMA_BASE_URL, show_default=True,
              help="Ollama base url")
@click.option('--default-model-manager', type=str, default=DEFAULT_MODEL_MANAGER, show_default=True,
              help="Default model manager to use when starting a new chat. If None, user will be asked to choose one")
@click.option('--default-model', type=str, default=DEFAULT_MODEL, show_default=True,
              help="Default model to use when starting a new chat. If None, the user will be asked to choose one")
@click.option('--default-model-config', type=str, default=None, show_default=True,
              help="Default model additional configuration given to the model when calling it")
@click.option('--history-max-length', type=int, default=DEFAULT_HISTORY_MAX_LENGTH, show_default=True,
              help="Maximum length of the history to include when answering a message using a model")
@click.option('--min-nb-chunk-to-show', type=int, default=DEFAULT_MIN_NB_CHUNK_TO_SHOW, show_default=True,
              help="The minimum number of chunks to show at the same time when streaming the answer of a model")
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
# @click.option('-lh', '--llmsherpa-host', type=str, default="", show_default=True, help="Telegram bot API token.")
# @click.option('-lp', '--llmsherpa-port', type=str, default="", show_default=True, help="Telegram bot API token.")
@pass_quackamollie_settings
@click.pass_context
def serve(ctx, settings: QuackamollieSettings, bot_token: str, admin_ids: List[int], moderator_ids: List[int],
          user_ids: List[int], data_dir: click.Path, ollama_base_url: Optional[str],
          default_model_manager: Optional[str], default_model: Optional[str], default_model_config: Optional[str],
          history_max_length: Optional[int], min_nb_chunk_to_show: int, db_protocol: str,
          db_username: Optional[str], db_password: Optional[str], db_host: str, db_port: Optional[int], db_name: str,
          db_url: Optional[str]):
    """ CLI command to serve Quackamollie bot which polls and answers Telegram messages.\f

        :param ctx: Click context to pass between commands of quackamollie
        :type ctx: click.Context

        :param settings: Quackamollie settings to pass between commands of quackamollie
        :type settings: QuackamollieSettings

        :param bot_token: Telegram bot API token
        :param bot_token: str

        :param admin_ids: A list of admin user ids separated by commas
        :param admin_ids: List[int]

        :param moderator_ids: A list of moderator user ids separated by commas
        :param moderator_ids: List[int]

        :param user_ids: A list of user ids separated by commas
        :param user_ids: List[int]

        :param data_dir: Data directory dedicated to Quackamollie's data
        :param data_dir: click.Path

        :param ollama_base_url: Ollama base url
        :param ollama_base_url: Optional[str]

        :param default_model_manager: Default model manager to use when starting a new chat.
                                      If None, user will be asked to choose one
        :param default_model_manager: Optional[str]

        :param default_model: Default model to use when starting a new chat.
                              If None, the user will be asked to choose one
        :param default_model: Optional[str]

        :param default_model_config: Default model additional configuration given to the model when calling it
        :param default_model_config: Optional[str]

        :param history_max_length: Maximum length of the history to include when answering a message using a model
        :param history_max_length: Optional[int]

        :param min_nb_chunk_to_show: The minimum number of chunks to show at the same time when streaming the answer
                                     of a model
        :param min_nb_chunk_to_show: int

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
    # Load Model Managers and ensure the given default model manager value are supported with current installation
    QuackamollieModelManagerRegistry().load_model_managers()
    if default_model_manager is not None:
        model_managers = QuackamollieModelManagerRegistry().model_managers
        if default_model_manager not in model_managers:
            raise click.BadParameter(f"No MetaQuackamollieModelManager found with name '{default_model_manager}'."
                                     f" Please ensure the name is correct and the associated package is installed"
                                     f" (typically with `pip install"
                                     f" quackamollie-{default_model_manager}-model-manager`)",
                                     param_hint="'--default-model-manager'")
    elif default_model is not None:
        raise click.BadParameter("Default model name is set however no default model manager is defined."
                                 " Please ensure a model manager is provided if a model name is given.",
                                 param_hint="'--default-model-manager'")

    # Add new configurations to context
    settings.bot_token = bot_token
    settings.admin_ids = admin_ids
    settings.moderator_ids = moderator_ids
    settings.user_ids = user_ids
    settings.data_dir = data_dir
    settings.ollama_base_url = ollama_base_url
    settings.default_model_manager = default_model_manager
    settings.default_model = default_model
    settings.default_model_config = default_model_config
    settings.history_max_length = history_max_length
    settings.min_nb_chunk_to_show = min_nb_chunk_to_show
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
    log.debug(f"Serve input settings are :"
              f"\n\tbot_token: {settings.anonymized_bot_token} [from {ctx.get_parameter_source('bot_token').name}]"
              f"\n\tadmin_ids: {settings.anonymized_admin_ids} [from {ctx.get_parameter_source('admin_ids').name}]"
              f"\n\tmoderator_ids: {settings.anonymized_moderator_ids}"
              f" [from {ctx.get_parameter_source('moderator_ids').name}]"
              f"\n\tuser_ids: {settings.anonymized_user_ids} [from {ctx.get_parameter_source('user_ids').name}]"
              f"\n\tauthorized_ids: {settings.anonymized_authorized_ids} [from INFERRED]"
              f"\n\tdata_dir: {settings.data_dir} [from {ctx.get_parameter_source('data_dir').name}]"
              f"\n\tollama_base_url: {settings.ollama_base_url}"
              f" [from {ctx.get_parameter_source('ollama_base_url').name}]"
              f"\n\tdefault_model_manager: {settings.default_model_manager}"
              f" [from {ctx.get_parameter_source('default_model_manager').name}]"
              f"\n\tdefault_model: {settings.default_model} [from {ctx.get_parameter_source('default_model').name}]"
              f"\n\tdefault_model_config: {settings.default_model_config}"
              f" [from {ctx.get_parameter_source('default_model_config').name}]"
              f"\n\thistory_max_length: {settings.history_max_length}"
              f" [from {ctx.get_parameter_source('history_max_length').name}]"
              f"\n\tmin_nb_chunk_to_show: {settings.min_nb_chunk_to_show}"
              f" [from {ctx.get_parameter_source('min_nb_chunk_to_show').name}]"
              f"\n\tdb_protocol: {settings.db_protocol} [from {ctx.get_parameter_source('db_protocol').name}]"
              f"\n\tdb_username: {settings.anonymized_db_username}"
              f" [from {ctx.get_parameter_source('db_username').name}]"
              f"\n\tdb_password: {settings.anonymized_db_password}"
              f" [from {ctx.get_parameter_source('db_password').name}]"
              f"\n\tdb_host: {settings.db_host} [from {ctx.get_parameter_source('db_host').name}]"
              f"\n\tdb_port: {settings.db_port} [from {ctx.get_parameter_source('db_port').name}]"
              f"\n\tdb_name: {settings.db_name} [from {ctx.get_parameter_source('db_name').name}]"
              f"\n\tdb_url: {settings.anonymized_db_url} [from {db_url_parameter_source}]")

    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Initialize bot
    settings.bot = Bot(token=bot_token)
    settings.dispatcher = Dispatcher()
    settings.commands = get_commands_list()

    # Initialize database connectors
    # cf. SQLAlchemy 2.0 documentation: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm
    settings.engine = create_async_engine(settings.db_url, echo=True)
    settings.session = async_sessionmaker(settings.engine, expire_on_commit=False)

    # Disable settings edition before launching asynchronous processing
    settings.enable_settings_edition = False

    log.debug("Start Quackamollie bot")
    asyncio.run(start_quackamollie_bot(settings, settings.bot, settings.dispatcher, settings.commands, settings.engine,
                                       settings.session))
