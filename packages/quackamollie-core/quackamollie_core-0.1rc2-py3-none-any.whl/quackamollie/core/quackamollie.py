# -*- coding: utf-8 -*-
__all__ = ["quackamollie"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import click
import coloredlogs
import logging
import os
import traceback

from datetime import datetime
from logging.config import dictConfig
from pyfiglet import Figlet
from typing import Optional
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from quackamollie.core import core_version
from quackamollie.core.constants import LOG_DIR_STR_TO_REPLACE
from quackamollie.core.cli.helpers.entry_point_command import get_commands_from_entry_points
from quackamollie.core.cli.helpers.logging import callback_verbosity_count_to_logging_level
from quackamollie.core.cli.settings import QuackamollieSettings, pass_quackamollie_settings
from quackamollie.core.defaults import DEFAULT_CONFIG_FILE, DEFAULT_LOG_DIR, DEFAULT_VERBOSITY

log = logging.getLogger(__name__)


@click.group(context_settings={'auto_envvar_prefix': 'QUACKAMOLLIE'},  # Enable environment variables starting with this
             commands=get_commands_from_entry_points('quackamollie.command'))
@click.help_option('-h', '--help')
@click.version_option(version=click.style(f'core_version={core_version}', bold=True))
@click.option('-v', '--verbose', count=True, default=DEFAULT_VERBOSITY, help="Enable verbose output",
              callback=callback_verbosity_count_to_logging_level)
@click.option('-c', '--config-file', type=click.Path(exists=True, dir_okay=False),
              default=DEFAULT_CONFIG_FILE, help='Configuration file path for the application')
@click.option('-l', '--log-dir', type=click.Path(exists=True, file_okay=False), default=DEFAULT_LOG_DIR,
              show_default=True, help="Dir path for logs")
@pass_quackamollie_settings
@click.pass_context
def quackamollie(ctx: click.Context, settings: QuackamollieSettings, verbose: int, config_file: click.Path,
                 log_dir: Optional[str]):
    """ Command line interface for quackamollie.\f

        :param ctx: Click context to pass between commands of quackamollie
        :type ctx: click.Context

        :param settings: Quackamollie settings to pass between commands of quackamollie
        :type settings: QuackamollieSettings

        :param verbose: Verbosity level, default: 0
        :type verbose: int

        :param config_file: Configuration file, default: Unset
        :type config_file: click.Path(exists=True, dir_okay=False)

        :param log_dir: Directory where to export logs. By default, it is unset so logs are prompted in console.
        :type log_dir: click.Path(exists=True, file_okay=False)
    """
    # Config file import section, inspired from stackoverflow answer https://stackoverflow.com/a/73669230/5498624
    settings.config_file = config_file
    if config_file is not None:  # Import config from file and set it as default map for sub-commands
        if os.path.exists(config_file):  # Existence should be ensured by click option parsing
            with open(config_file, 'r') as f:
                config = load(f.read(), Loader=Loader)
            ctx.default_map = config.copy()  # Set subcommands default values
            if 'logging' in ctx.default_map:  # Remove logging entry from the default map because it is handled now
                del ctx.default_map['logging']
            settings.config = config  # Save the whole configuration file content
            settings.logging_config = config.get('logging', None)  # Expose logging configuration
            if log_dir is None:  # Get logging directory from configuration, if not overridden through option
                log_dir = config.get('log_dir', None)
                if log_dir is not None and not os.path.isdir(log_dir):  # If defined, we ensure the repository exists
                    raise click.BadParameter(f"Directory '{log_dir}' does not exist.",
                                             param_hint='"-l" / "--log-dir"')
    else:
        settings.config = None
        settings.logging_config = None

    # Logging set up section
    if settings.logging_config is not None:  # Init logging from the 'logging' section of the config file, if defined
        # If `log_dir` is defined, try to replace LOG_DIR_STR_TO_REPLACE value occurrences in logging configuration
        # by the specified log dir
        if log_dir is not None and 'handlers' in settings.logging_config:
            for handler_name, d_handler_spec in settings.logging_config['handlers'].items():
                for key, val in d_handler_spec.items():
                    if type(val) is str and LOG_DIR_STR_TO_REPLACE in val:
                        settings.logging_config['handlers'][handler_name][key] = val.replace(LOG_DIR_STR_TO_REPLACE,
                                                                                             log_dir)

        # If verbosity is override from command line or environment variable, we override it in settings.logging_config
        if (verbose != logging.NOTSET and 'root' in settings.logging_config and
                isinstance(settings.logging_config['root'], dict)):
            settings.logging_config['root']['level'] = logging.getLevelName(verbose)

        # Setup logging using parsed configuration
        try:
            dictConfig(settings.logging_config)
        except ValueError as e:
            if LOG_DIR_STR_TO_REPLACE in traceback.format_exc():
                raise click.MissingParameter(f"The string '{LOG_DIR_STR_TO_REPLACE}' is used in configuration"
                                             f" file, however no log_dir was given in parameter",
                                             param_hint='"-l" / "--log-dir"', param_type="click.Path")
            else:
                raise e

        if verbose == logging.NOTSET:  # Get the verbosity directly from logger if not override
            settings.verbose = logging.getLogger().getEffectiveLevel()
        else:  # Use the command line verbosity if set
            settings.verbose = verbose
    elif verbose != logging.NOTSET:  # No logging config section, we set logging from verbose option, if it is set
        settings.verbose = verbose  # Use the command line verbosity if set
        if log_dir is None:
            coloredlogs.install(level=verbose)  # Use coloredlogs to improve readability
        else:  # If the log_dir is set, we export logs using daily timestamp filenames
            logging.basicConfig(level=verbose, filename='{}/{:%Y-%m-%d}.log'.format(log_dir, datetime.now()))
    else:  # The default case is a simple `logging.basicConfig` call, we set logging.CRITICAL so it
        settings.verbose = logging.CRITICAL  # Use the highest verbosity level if not set
        logging.basicConfig(level=settings.verbose)

    # Set up Quackamollie context
    settings.log_dir = log_dir

    # Print the verbosity level if it is set
    if settings.verbose != logging.NOTSET and settings.verbose < logging.CRITICAL:
        click.echo(click.style(f'Verbose logging is enabled. (LEVEL={settings.verbose})', fg='yellow'))

    # Print a Figlet of the program name if the verbosity is less than error, just for style
    if settings.verbose != logging.NOTSET and settings.verbose < logging.CRITICAL:
        click.echo(Figlet(font='slant').renderText('Quackamollie'))

    # Log input settings for debug use, do NOT show raw configuration because it can contain sensitive data
    log.debug(f"Quackamollie input settings are :"
              f"\n\tverbose: {settings.verbose} [from {ctx.get_parameter_source('verbose').name}]"
              f"\n\tconfig_file: {settings.config_file} [from {ctx.get_parameter_source('config_file').name}]"
              f"\n\tlog_dir: {settings.log_dir} [from {ctx.get_parameter_source('log_dir').name}]")
