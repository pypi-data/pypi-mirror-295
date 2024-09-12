# -*- coding: utf-8 -*-
""" Module for the `User Settings` sub-menu of the `/settings` Telegram bot command """
__all__ = ["user_settings_router", "user_settings_callback_handler", "document_management_callback_handler"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from quackamollie.core.bot.decorator.permissions import permission_authorized
from quackamollie.core.bot.decorator.user_chat_registered import ensure_user_chat_registered
from quackamollie.core.bot.menu.settings_menu import SettingsCallbackData

user_settings_router = Router()


@user_settings_router.callback_query(SettingsCallbackData.filter(F.name == "user"))
@permission_authorized
@ensure_user_chat_registered
async def user_settings_callback_handler(query: CallbackQuery):
    """ Callback query handler for the "User Settings" section of the bot. Allow modification of the user app settings.

        :param query: A callback query given by aiogram
        :type query: CallbackQuery
    """
    user_settings_builder = InlineKeyboardBuilder()
    user_settings_builder.row(
        InlineKeyboardButton(text="📄 Documents Management",
                             callback_data=SettingsCallbackData(name="document_management").pack()),
        InlineKeyboardButton(text="⬅️ Go back",
                             callback_data=SettingsCallbackData(name="settings_root").pack()),
    )

    await query.message.edit_text("👤 <b>User Settings</b>\n\n📄 <i>Documents Management</i> [Coming Soon] \n"
                                  "Manage and share your documents across your different chats with me",
                                  reply_markup=user_settings_builder.as_markup(),
                                  parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@user_settings_router.callback_query(SettingsCallbackData.filter(F.name == "document_management"))
@permission_authorized
@ensure_user_chat_registered
async def document_management_callback_handler(query: CallbackQuery):
    """ Callback query handler for the "User Settings/Documents Management" section of the bot.
        Allow modification of the user documents and associated sharing rules.

        :param query: A callback query given by aiogram
        :type query: CallbackQuery
    """
    await query.answer("Not implemented yet, coming soon...")
