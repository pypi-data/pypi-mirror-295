# -*- coding: utf-8 -*-
""" Module for the `App Settings` sub-menu of the `/settings` Telegram bot command """
__all__ = ["app_settings_router", "app_settings_callback_handler"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from aiogram import F, Router
from aiogram.types import CallbackQuery

from quackamollie.core.bot.decorator.permissions import permission_moderator
from quackamollie.core.bot.decorator.user_chat_registered import ensure_user_chat_registered
from quackamollie.core.bot.menu.settings_menu import SettingsCallbackData

app_settings_router = Router()


@app_settings_router.callback_query(SettingsCallbackData.filter(F.name == "app"))
@permission_moderator
@ensure_user_chat_registered
async def app_settings_callback_handler(query: CallbackQuery):
    """ Callback query handler for the "App Settings" section of the bot

        :param query: A callback query given by aiogram
        :type query: CallbackQuery
    """
    await query.answer("Not implemented yet, coming soon...")
