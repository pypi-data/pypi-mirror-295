# -*- coding: utf-8 -*-
""" Module for the `Info` section of the `/settings` Telegram bot command """
__all__ = ["info_router", "info_callback_handler"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from quackamollie.core import core_version
from quackamollie.core.bot.bot_info import QuackamollieBotData
from quackamollie.core.bot.decorator.permissions import permission_authorized
from quackamollie.core.bot.menu.settings_menu import SettingsCallbackData
from quackamollie.core.cli.settings import pass_quackamollie_settings, QuackamollieSettings

info_router = Router()


@info_router.callback_query(SettingsCallbackData.filter(F.name == "info"))
@permission_authorized
@pass_quackamollie_settings
async def info_callback_handler(quackamollie_settings: QuackamollieSettings, query: CallbackQuery):
    """ Callback query handler for the "Info" section of the bot. Show general information about the bot and if the
        user is an admin or a moderator, it shows also the current running version of `quackamollie-core`.

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param query: A callback query given by aiogram
        :type query: CallbackQuery
    """
    mention = QuackamollieBotData().bot_mention  # Get the bot name with '@'
    info: str = f"The bot {mention} is an instance of the open source project <i>Quackamollie</i>."

    # If the user is an admin or a moderator, we show the current core version
    user_id: int = query.from_user.id
    if user_id in quackamollie_settings.admin_ids or user_id in quackamollie_settings.moderator_ids:
        info += f" This current instance uses <code>quackamollie-core</code> version <code>{core_version}</code>."

    info += ("\n\n<i>Quackamollie</i> is a project by the"
             " <a href='https://gitlab.com/forge_of_absurd_ducks'>Forge of Absurd Ducks</a>.\n"
             "<a href='https://gitlab.com/forge_of_absurd_ducks/quackamollie/quackamollie'>Source code</a> is under"
             " <a href='https://gitlab.com/forge_of_absurd_ducks/quackamollie/quackamollie/LICENSE'>MIT License</a>.")

    await query.message.answer(info, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    await query.answer()  # To complete CallbackQuery loading bar
