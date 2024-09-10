# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from quackamollie.core.utils.str_management import camel_to_snake, sanitize_username


def test_camel_to_snake():
    """ Test `camel_to_snake()` function which convert a CamelCaseString to a snake_case_string

        Arrange/Act: Run the `camel_to_snake()` function
        Assert: The output matches what is expected
    """
    snake_res = camel_to_snake("TestCamelString")
    assert snake_res == "test_camel_string", (f"`camel_to_snake()` function didn't return expected 'test_camel_string'"
                                              f" and returned instead '{snake_res}'")


def test_sanitize_username():
    """ Test `sanitize_username()` function which sanitize a username by removing unwanted characters

        Arrange/Act: Run the `sanitize_username()` function
        Assert: The output matches what is expected
    """
    sanitized_res = sanitize_username("`user`_\"name\"_'with'_{weird}_([characters])")
    assert sanitized_res == "user_name_with_weird_characters", \
        (f"`sanitize_username()` function didn't return expected 'user_name_with_weird_characters'"
         f" and returned instead '{sanitized_res}'")
