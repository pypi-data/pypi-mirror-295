# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import os
import pytest

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import Optional

from quackamollie.core.cli.helpers.db_url_config import get_db_url_from_config
from quackamollie.core.defaults import DEFAULT_DB_PROTOCOL, DEFAULT_DB_HOST, DEFAULT_DB_NAME

TEST_LOG_DIRS = ['tests/logs/', 'tests/logs_app_config/', 'tests/logs_env/']


def pytest_addoption(parser):
    parser.addoption("--db-protocol", action="store", type=str, default=DEFAULT_DB_PROTOCOL,
                     help="Run database online tests using this protocol.")
    parser.addoption("--db-host", action="store", type=str, default=DEFAULT_DB_HOST,
                     help="Run database online tests using this host.")
    parser.addoption("--db-name", action="store", type=str, default=DEFAULT_DB_NAME,
                     help="Run database online tests using this name.")
    parser.addoption("--db-username", action="store", type=str, default=None,
                     help="Run database online tests using this username.")
    parser.addoption("--db-password", action="store", type=str, default=None,
                     help="Run database online tests using this password.")
    parser.addoption("--db-port", action="store", type=str, default=None,
                     help="Run database online tests using this port.")
    parser.addoption("--db-url", action="store", type=str, default=None,
                     help="Run online tests with database using this database URL. If not defined, it will be build"
                          " from `--db-protocol`, `--db-host` and `--db-name`")
    parser.addoption("--dry-run", action="store_true", default=False, help="Run only the outline tests.")
    parser.addoption("--all", action="store_true", default=False, help="Run all tests.")


@pytest.fixture(scope='session')
def db_protocol(request) -> str:
    return request.config.getoption("--db-protocol")


@pytest.fixture(scope='session')
def db_host(request) -> str:
    return request.config.getoption("--db-host")


@pytest.fixture(scope='session')
def db_name(request) -> str:
    return request.config.getoption("--db-name")


@pytest.fixture(scope='session')
def db_username(request) -> Optional[str]:
    return request.config.getoption("--db-username")


@pytest.fixture(scope='session')
def db_password(request) -> Optional[str]:
    return request.config.getoption("--db-password")


@pytest.fixture(scope='session')
def db_port(request) -> Optional[str]:
    return request.config.getoption("--db-port")


@pytest.fixture(scope='session')
def db_url(request, db_protocol, db_host, db_name, db_username, db_password, db_port) -> Optional[str]:
    _db_url = request.config.getoption("--db-url")
    if _db_url is None:
        if db_protocol is None or db_host is None or db_name is None:
            return None
        else:
            return get_db_url_from_config(db_protocol, db_host, db_name, db_username, db_password, db_port)
    else:
        return _db_url


@pytest.fixture(scope='session')
def dry_run(request, db_url) -> bool:
    if db_url is None:
        return True
    else:
        return request.config.getoption("--dry-run")


@pytest.fixture(scope='session')
def run_all(request) -> bool:
    return request.config.getoption("--all")


@pytest.fixture(scope='session')
def database_client(dry_run, run_all, db_url) -> Optional[async_sessionmaker[AsyncSession]]:
    if dry_run and not run_all:
        return None
    elif db_url is None:
        return None
    else:
        engine = create_async_engine(db_url, echo=True)
        return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope='session')
def ensure_log_dirs_exist():
    """ Fixture to ensure that TEST_LOG_DIRS directories exists. """
    for fp_log_dir in TEST_LOG_DIRS:
        os.makedirs(fp_log_dir, exist_ok=True)
