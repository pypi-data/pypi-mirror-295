# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from datetime import datetime

from quackamollie.core.utils.timestamp_versioning import generate_timestamp_version


def test_generate_timestamp_version():
    """ Test `generate_timestamp_version()` function which create a timestamp from the current time

        Arrange/Act: Run the `generate_timestamp_version()` function
        Assert: The output is of type str, and it can be cast back to datetime format
    """
    timestamp_version = generate_timestamp_version()
    assert isinstance(timestamp_version, str), "The output of `generate_timestamp_version()` should be a string"

    datetime_res = datetime.strptime(timestamp_version, "%y.%m.%d-%H.%M.%S")
    assert isinstance(datetime_res, datetime), ("The parsing of the generated timestamp should have created a valid"
                                                " datetime object")
