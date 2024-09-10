# -*- coding: utf-8 -*-
""" Module for the `Chat Settings` sub-menu of the `/settings` Telegram bot command """
__all__ = ["chat_settings_router", "chat_settings_callback_handler", "model_management_callback_handler",
           "model_chosen_callback_handler"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import logging

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Dict, List, Optional

from quackamollie.core.bot.decorator.permissions import permission_authorized
from quackamollie.core.bot.decorator.user_chat_registered import ensure_user_chat_registered
from quackamollie.core.bot.menu.settings_menu import SettingsCallbackData
from quackamollie.core.cli.settings import pass_quackamollie_settings, QuackamollieSettings
from quackamollie.core.model_manager_registry.model_manager_registry import QuackamollieModelManagerRegistry
from quackamollie.core.enum.model_family_icon import ModelFamilyIcon
from quackamollie.core.database.model import ChatSetting, ModelConfig, ModelManagerType
from quackamollie.core.enum.chat_type import ChatType

log = logging.getLogger(__name__)

chat_settings_router = Router()


@chat_settings_router.callback_query(SettingsCallbackData.filter(F.name == "chat"))
@permission_authorized
@ensure_user_chat_registered
@pass_quackamollie_settings
async def chat_settings_callback_handler(quackamollie_settings: QuackamollieSettings, query: CallbackQuery):
    """ Callback query handler for the "Chat Settings" section of the bot

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param query: A callback query given by aiogram
        :type query: CallbackQuery
    """
    # Get database session from settings
    async_session = quackamollie_settings.session

    # Get model manager registry to parse class names to user readable names
    model_manager_registry = QuackamollieModelManagerRegistry()

    # Get chat info from message
    chat_id: int = query.message.chat.id
    chat_type: ChatType = ChatType[query.message.chat.type]

    # Get from database the model manager, model name, model config and possible chat type override
    async with async_session() as session:
        # Get chat settings for the current chat
        chat_setting_result = await session.execute(select(ChatSetting).where(
            ChatSetting.chat_id == chat_id
        ).limit(1).options(selectinload(ChatSetting.model_config)))
        chat_setting: Optional[ChatSetting] = chat_setting_result.scalars().first()

        # Get model settings for the current chat
        if chat_setting.model_config is not None:
            model_name = chat_setting.model_config.model_name
            model_config = chat_setting.model_config.config
            model_manager = await chat_setting.model_config.awaitable_attrs.model_manager_type
            model_manager_class = model_manager.model_manager_class
            model_manager_name = model_manager_registry.class_name_to_entrypoint_name.get(model_manager_class,
                                                                                          "Unsupported Model Manager")
        else:
            model_name = "[from defaults]"
            model_config = "[from defaults]"
            model_manager_name = "[from defaults]"

        # Get possible chat type override from database, if not already in a private chat
        if chat_type != ChatType.private:
            chat_type_override: Optional[ChatType] = chat_setting.chat_type_override
            if chat_type_override is not None:
                chat_type = chat_type_override

    settings_message = ("💬 <b>Chat Settings</b>\n\n🧠 <i>Model Management</i>\nChange the model to use in this chat\n\n"
                        "⚙ <i>Default settings</i>\n"
                        f"  - Model manager: <code>{quackamollie_settings.default_model_manager}</code>\n"
                        f"  - Model: <code>{quackamollie_settings.default_model}</code>\n"
                        f"  - Model config: <code>{quackamollie_settings.default_model_config}</code>\n\n"
                        "💬 <i>Current chat settings</i>\n"
                        f"  - Model manager: <code>{model_manager_name}</code>\n"
                        f"  - Model: <code>{model_name}</code>\n"
                        f"  - Model config: <code>{model_config}</code>")

    if chat_type != ChatType.private and chat_type_override is not None:
        settings_message += f"\n  - Chat type override: <code>{chat_type.value}</code>"
    else:
        settings_message += f"\n  - Chat type: <code>{chat_type.value}</code>"

    # Construct the inline keyboard builder
    user_settings_builder = InlineKeyboardBuilder()
    user_settings_builder.row(
        InlineKeyboardButton(text="🧠 Model Management",
                             callback_data=SettingsCallbackData(name="model_management").pack()),
        InlineKeyboardButton(text="⬅️ Go back",
                             callback_data=SettingsCallbackData(name="settings_root").pack()),
    )

    # Answer the message with constructed answer and inline keyboard builder
    await query.message.edit_text(settings_message,
                                  reply_markup=user_settings_builder.as_markup(),
                                  parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@chat_settings_router.callback_query(SettingsCallbackData.filter(F.name == "model_management"))
@permission_authorized
@ensure_user_chat_registered
async def model_management_callback_handler(query: CallbackQuery):
    """ Callback query handler for the "User Settings/Model Management" section of the bot.
        Allow modification of the current chat model.

        :param query: A callback query given by aiogram
        :type query: CallbackQuery
    """
    model_management_builder = InlineKeyboardBuilder()
    model_manager_registry = QuackamollieModelManagerRegistry()
    all_model_families: List[ModelFamilyIcon] = []
    for model_manager_name, model_manager_class in model_manager_registry.model_managers.items():
        log.debug(f"model_manager_class.get_model_list() = {await model_manager_class.get_model_list()}")
        formatted_model_manager_name: str = (f"{''.join([family.value for family in model_manager_class.families])}"
                                             f" {model_manager_name}")
        log.debug(f"formatted_model_manager_name={formatted_model_manager_name}")
        model_families: Dict[str, List[ModelFamilyIcon]] = await model_manager_class.get_model_families()
        log.debug(f"model_families={model_families}")
        for model_name, families in model_families.items():
            all_model_families.extend(families)
            formatted_model_name: str = f"{''.join([family.value for family in families])} {model_name}"
            formatted_model_name = f"{formatted_model_manager_name} | {formatted_model_name}"
            sane_model_name: str = model_name.replace(':', '__')

            model_settings_callback_data = SettingsCallbackData(name=f"model/{model_manager_name}/{sane_model_name}")
            model_management_builder.row(InlineKeyboardButton(text=formatted_model_name,
                                                              callback_data=model_settings_callback_data.pack()))

    model_management_builder.row(InlineKeyboardButton(text="⬅️ Go back",
                                                      callback_data=SettingsCallbackData(name="chat").pack()))

    families_legend: str = ""
    for family in set(all_model_families):
        families_legend += f"\n{family.value} = {family.description}"

    if not families_legend:
        families_legend = "\n❌ No Model legend found"

    await query.message.edit_text(f"🧠 <b>Model Management</b>\n\nPlease, choose a model for the current chat"
                                  f" among those listed\n\n<i>Legend</i>{families_legend}",
                                  reply_markup=model_management_builder.as_markup(),
                                  parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@chat_settings_router.callback_query(SettingsCallbackData.filter(F.name.startswith("model/")))
@permission_authorized
@ensure_user_chat_registered
@pass_quackamollie_settings
async def model_chosen_callback_handler(quackamollie_settings: QuackamollieSettings, query: CallbackQuery,
                                        callback_data: SettingsCallbackData):
    """ Callback query handler for the "User Settings/Model Management" section of the bot.
        Allow modification of the current chat model.

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param query: A callback query given by aiogram
        :type query: CallbackQuery

        :param callback_data: Callback data parsed and filtered by aiogram
        :type callback_data: SettingsCallbackData
    """
    original_name: str = callback_data.name.replace('__', ':')
    _, model_manager_name, model_name = original_name.split('/')

    model_manager_registry = QuackamollieModelManagerRegistry()
    model_manager_class = model_manager_registry.model_managers[model_manager_name]

    # Get chat info
    chat_id: int = query.message.chat.id

    # Get database session from settings
    async_session = quackamollie_settings.session

    # Set the current configuration for the chat in the database
    async with async_session() as session:
        model_manager_result = await session.execute(select(ModelManagerType.id).where(
            ModelManagerType.model_manager_class == model_manager_class.__name__
        ).limit(1))
        model_manager_id = model_manager_result.scalars().one()
        log.debug(f"model_manager_id={model_manager_id}")

        model_config_result = await session.execute(select(ModelConfig).where(
            ModelConfig.model_manager_type_id == model_manager_id
        ).where(
            ModelConfig.model_name == model_name
        ).limit(1))
        model_config: Optional[ModelConfig] = model_config_result.scalars().first()
        log.debug(f"model_config={model_config}")

        chat_setting_result = await session.execute(select(ChatSetting).where(
            ChatSetting.chat_id == chat_id
        ).limit(1).options(selectinload(ChatSetting.model_config)))
        chat_setting: Optional[ChatSetting] = chat_setting_result.scalars().first()
        log.debug(f"chat_setting={chat_setting}")

        if model_config is None:
            chat_setting.model_config = ModelConfig(config_name=model_name.split(':', 1)[0],
                                                    model_manager_type_id=model_manager_id,
                                                    model_name=model_name)
        else:
            chat_setting.model_config = model_config
        await session.commit()

    model_builder = InlineKeyboardBuilder()
    model_builder.row(InlineKeyboardButton(text="⬅️ Go back", callback_data=SettingsCallbackData(name="chat").pack()))
    await query.message.edit_text(
        query.message.text + f"\n\nModel <b>successfully</b> set to <code>{model_manager_name}</code>"
                             f" | <code>{model_name}</code>",
        reply_markup=model_builder.as_markup(), parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )
