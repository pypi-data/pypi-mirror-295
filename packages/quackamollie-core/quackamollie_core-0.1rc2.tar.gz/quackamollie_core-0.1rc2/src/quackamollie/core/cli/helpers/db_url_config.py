# -*- coding: utf-8 -*-
__all__ = ["get_db_url_from_config", "anonymize_database_url"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import re

from typing import Optional


def get_db_url_from_config(db_protocol: str, db_host: str, db_name: str, db_username: Optional[str],
                           db_password: Optional[str], db_port: Optional[int]) -> str:
    """ Construct database URL from URL fields

        :param db_protocol: Database protocol, must be a protocol supported by SQLAlchemy
        :type db_protocol: str

        :param db_host: Hostname of the database
        :type db_host: str

        :param db_name: Name of the database
        :type db_name: str

        :param db_username: Username for database connection
        :type db_username: Optional[str]

        :param db_password: Password for database connection
        :type db_password: Optional[str]

        :param db_port: Port of the database
        :type db_port: Optional[str]

        :return: The URL of the database in the format
                 `{db_protocol}://{db_username}:{db_password}@{}:{db_port}/{db_name}`
        :rtype: str
    """
    db_url: str = f"{db_protocol}://"
    if db_username is not None:
        if db_password is None:
            db_url += f"{db_username}@"
        else:
            db_url += f"{db_username}:{db_password}@"
    db_url += db_host
    if db_port is not None:
        db_url += f":{db_port}"
    db_url += f"/{db_name}"
    return db_url


def anonymize_database_url(db_url: str) -> str:
    """ Hide the username and password of a given database URL

        :param db_url: The database URL to anonymize, typically `postgres://user:password@host/database`
        :type db_url: str

        :return: The anonymized URL, typically `postgres://host/database` or `postgres://us****@host/database` or
                 `postgres://us****:****@host/database`. The number of asterisks is a constant to not divulge data.
        :rtype: str
    """
    db_url_regex_userpass = re.search(r"^.*://(?P<userpass>.*)@.*$", db_url)
    if db_url_regex_userpass is not None and 'userpass' in db_url_regex_userpass.groupdict():
        userpass = db_url_regex_userpass.groupdict()['userpass']
        return db_url.replace(userpass, f"{userpass[:2]}****{':****' if ':' in userpass else ''}")
    else:
        return db_url
