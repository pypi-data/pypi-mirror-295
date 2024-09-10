# -*- coding: utf-8 -*-
__all__ = ["SettingsCallbackData", "get_settings_menu_root"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from quackamollie.core.enum.chat_type import ChatType
from quackamollie.core.enum.role_type import AppRoleType


class SettingsCallbackData(CallbackData, prefix="settings"):
    name: str


def get_settings_menu_root(chat_type: ChatType, app_role_type: AppRoleType) -> InlineKeyboardBuilder:
    """ Build the root of the settings menu depending on given parameters

        :param chat_type: The current chat type
        :type chat_type: ChatType

        :param app_role_type: The current user's application role
        :type app_role_type: AppRoleType

        :return: The constructed root settings menu
        :rtype: InlineKeyboardBuilder
    """
    settings_builder = InlineKeyboardBuilder()
    settings_builder.row(InlineKeyboardButton(text="ℹ About",
                                              callback_data=SettingsCallbackData(name="info").pack()),
                         InlineKeyboardButton(text="💬 Chat Settings",
                                              callback_data=SettingsCallbackData(name="chat").pack()))
    if chat_type == ChatType.private:
        user_settings = InlineKeyboardButton(text="👤 User Settings",
                                             callback_data=SettingsCallbackData(name="user").pack())
        if app_role_type == AppRoleType.moderator or app_role_type == AppRoleType.admin:
            settings_builder.row(user_settings,
                                 InlineKeyboardButton(text="️⚙ App Settings",
                                                      callback_data=SettingsCallbackData(name="app").pack()))
        else:
            settings_builder.add(user_settings)

    return settings_builder


def get_settings_menu_root_description(chat_type: ChatType, app_role_type: AppRoleType) -> str:
    """ Build the description of the settings menu depending on given parameters

        :param chat_type: The current chat type
        :type chat_type: ChatType

        :param app_role_type: The current user's application role
        :type app_role_type: AppRoleType

        :return: The constructed description of the menus in the settings root menu
        :rtype: str
    """
    menus_description = ("⚙ <b>Settings</b>\n\nℹ <i>About</i>\nDisplay general information about the bot\n\n"
                         "💬 <i>Chat Settings</i>\nSettings of the current chat, like choosing a model\n\n")
    if chat_type == ChatType.private:
        menus_description += "👤 <i>User Settings</i>\nSettings of the user across all chats\n\n"
        if app_role_type == AppRoleType.moderator or app_role_type == AppRoleType.admin:
            menus_description += "⚙ <i>App Settings</i>\nAdmin global settings of the application\n\n"

    return menus_description
