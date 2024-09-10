# -*- coding: utf-8 -*-
__all__ = ["MetaQuackamollieModelManager"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI", "ruecat"]

import base64
import io
import logging
import re
import time
import traceback

from abc import ABCMeta, abstractmethod
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from asyncio.exceptions import TimeoutError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Any, Dict, List, Optional, Type

from quackamollie.core.bot.bot_info import QuackamollieBotData
from quackamollie.core.cli.settings import get_settings_from_context, QuackamollieSettings
from quackamollie.core.database.model import ChatMessage
from quackamollie.core.enum.model_family_icon import ModelFamilyIcon
from quackamollie.core.meta.model.meta_quackamollie_model import MetaQuackamollieModel

log = logging.getLogger(__name__)


class MetaQuackamollieModelManager(metaclass=ABCMeta):
    """ Metaclass for model managers managed by the `QuackamollieModelManagerRegistry` """

    families: List[ModelFamilyIcon]
    _model_list: None | List[str] = None
    _model_families: None | Dict[str, List[ModelFamilyIcon]] = None
    _regex_end_sentence: re.Pattern = re.compile(r"[-?!.;\n]")

    @classmethod
    @abstractmethod
    async def get_model_list(cls) -> List[str]:
        """ Discover the models available for the model manager at runtime asynchronously

            :return: A list of available models for the model manager
            :rtype: List[str]
        """
        raise NotImplementedError("Abstract method 'get_model_list' not implemented.")

    @classmethod
    @abstractmethod
    async def get_model_families(cls) -> Dict[str, List[ModelFamilyIcon]]:
        """ Discover the models families available for the model manager at runtime asynchronously

            :return: A dict with values the list of families indexed by model name
            :rtype: Dict[str, List[ModelFamilyIcon]]
        """
        raise NotImplementedError("Abstract method 'get_model_families' not implemented.")

    @classmethod
    @abstractmethod
    def parse_chat_history(cls, chat_messages: Optional[List[ChatMessage]]) -> List:
        """ Parse the chat history given as a list of `ChatMessage` from the database model to a list compatible with
            the model manager's models.

            :param chat_messages: A list of `ChatMessage` from the database model
            :param chat_messages: Optional[List[ChatMessage]]

            :return: A list of messages formatted to be compatible with the model manager's models.
            :rtype: List
        """
        raise NotImplementedError("Abstract method 'parse_chat_history' not implemented.")

    @classmethod
    @abstractmethod
    async def get_model_class(cls, model_name: str) -> Optional[Type[MetaQuackamollieModel]]:
        """ Get the model class from the model name

            :param model_name: Name of the model as listed by `cls.get_model_list`
            :type model_name: str

            :return: A subclass of MetaQuackamollieModel
            :rtype: Optional[Type[MetaQuackamollieModel]]
        """
        raise NotImplementedError("Abstract method 'get_model_class' not implemented.")

    @classmethod
    @abstractmethod
    def reset(cls):
        """ Reset the model manager dynamic fields to force reloading models. Be careful if used asynchronously """
        raise NotImplementedError("Abstract method 'reset' not implemented.")

    @classmethod
    async def request_model(cls, model_manager_name: str, model_name: str, model_config: Any, message: Message):
        """ Request a LLM model with a given message and stream the response

            :param model_manager_name: The user readable name of the current model manager,
                                       as registered in the `QuackamollieModelManagerRegistry`
            :type model_manager_name: str

            :param model_name: Name of the model as listed by `cls.get_model_list`
            :type model_name: str

            :param model_config: Additional configuration given as a string through CLI or Telegram `App Settings`
                                 and retrieved from the database
            :type model_config: Any

            :param message: The message as given by aiogram router
            :type message: Message
        """
        # Get mention and bot ID from pre-initialized bot data
        mention = QuackamollieBotData().bot_mention
        bot_id = QuackamollieBotData().bot_id

        # Remove the mention from the message or from the caption if no message
        if message.text:
            text_clean = message.text.replace(mention, "").strip()
        else:
            text_clean = message.caption.replace(mention, "").strip()

        # Get settings to get the database async session maker, the aiogram bot, history and streaming config
        quackamollie_settings: QuackamollieSettings = get_settings_from_context()
        quackamollie_bot: Bot = quackamollie_settings.bot
        async_session = quackamollie_settings.session
        history_max_length: Optional[int] = quackamollie_settings.history_max_length
        min_nb_chunk_to_show: int = quackamollie_settings.min_nb_chunk_to_show

        # Get user info from message
        user_id: int = message.from_user.id

        # Get chat info from message
        chat_id: int = message.chat.id

        # Parse images in base64 format (classically supported by LLM)
        images_base64: List[str] = []
        if message.content_type == 'photo':
            for photo in message.photo:
                image_buffer = io.BytesIO()
                await quackamollie_bot.download(photo, destination=image_buffer)
                images_base64.append(base64.b64encode(image_buffer.getvalue()).decode('utf-8'))

        # Get the message history and save current user message to the database
        async with async_session() as session:
            async with session.begin():
                # Get active chat history from the database in DESC order to be sure to get the newest messages
                # even when applying a limit
                if history_max_length is None:
                    chat_setting_result = await session.execute(select(ChatMessage).where(
                        ChatMessage.chat_id == chat_id
                    ).where(
                        ChatMessage.active
                    ).order_by(ChatMessage.sent_at_datetime.desc()).options(
                        selectinload(ChatMessage.user)
                    ))
                else:
                    chat_setting_result = await session.execute(select(ChatMessage).where(
                        ChatMessage.chat_id == chat_id
                    ).where(
                        ChatMessage.active
                    ).limit(history_max_length).order_by(ChatMessage.sent_at_datetime.desc()).options(
                        selectinload(ChatMessage.user)
                    ))
                chat_messages: Optional[List[ChatMessage]] = list(chat_setting_result.scalars().all())

                # Reverse the list order if not None and not empty, so the newest messages will be at the end
                if chat_messages:
                    chat_messages.reverse()

                # Construct the list of messages in a format supported by the current model manager
                chat_history: List = cls.parse_chat_history(chat_messages)

                # Save the new user message in the database, now that we have constructed the past message list
                new_chat_message = ChatMessage(id=message.message_id, user_id=user_id, chat_id=chat_id,
                                               content=text_clean, sent_at_datetime=message.date.replace(tzinfo=None),
                                               active=True)
                session.add(new_chat_message)

        # Get the current model class
        model_class: Optional[Type[MetaQuackamollieModel]] = await cls.get_model_class(model_name)

        # Raise an error and message to the user if the model is not found
        if model_class is None:
            error_msg = f"No model found with name '{model_name}' for the model manager `{model_manager_name}`"
            log.warning(error_msg)
            return await quackamollie_bot.send_message(chat_id=message.chat.id, text=error_msg,
                                                       reply_to_message_id=message.message_id,
                                                       parse_mode=ParseMode.MARKDOWN)

        # Inform the user that we are starting to answer its message using the LLM model
        await quackamollie_bot.send_chat_action(message.chat.id, "typing")
        log.debug(f"Start streaming the answer to user '{user_id}' in chat '{chat_id}' using"
                  f" model manager '{model_manager_name} and model '{model_name}'")

        # Answer the user message by streaming the answer from the model_class
        sent_message: Optional[Message] = None
        full_answer: str = ""
        clean_full_answer: str = ""
        nb_chunk_not_shown: int = 0
        try:
            start_time = time.time()  # To measure elapsed time
            async for chunk, is_done in model_class.astream_answer(text_clean, chat_history, model_config=model_config,
                                                                   model_name=model_name, images_base64=images_base64):
                # Append new chunk to the full answer and then clean full answer
                if chunk is not None:
                    full_answer += chunk
                    clean_full_answer = full_answer.strip()

                # If we received a new chunk as part of the stream
                if not is_done:
                    if chunk is None or not clean_full_answer:
                        continue  # To avoid bad requests due to an empty message text or an invalid chunk

                    # Edit text sentence by sentence to limit network calls or every `min_nb_chunk_to_show` chunk
                    if cls._regex_end_sentence.findall(chunk) or nb_chunk_not_shown >= min_nb_chunk_to_show:
                        try:
                            # If we didn't already send a message, we send a new one
                            if sent_message is None:
                                sent_message = await quackamollie_bot.send_message(
                                    chat_id=message.chat.id,
                                    text=clean_full_answer,
                                    reply_to_message_id=message.message_id,
                                    parse_mode=ParseMode.MARKDOWN
                                )
                                nb_chunk_not_shown = 0
                            # Else we edit the message sent with new chunk
                            elif sent_message.text != clean_full_answer:
                                sent_message = await quackamollie_bot.edit_message_text(
                                    chat_id=message.chat.id,
                                    message_id=sent_message.message_id,
                                    text=clean_full_answer,
                                    parse_mode=ParseMode.MARKDOWN
                                )
                                nb_chunk_not_shown = 0
                        except TelegramBadRequest:
                            # To avoid intermediary bad requests due to markdown specials not closed, like only one `*`
                            nb_chunk_not_shown += 1
                            continue
                    else:
                        nb_chunk_not_shown += 1
                # Else, this is the final chunk
                else:
                    # Compute elapsed time
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    # If we didn't already send a message, we send a new one or state that no text answer was given
                    if sent_message is None:
                        if not clean_full_answer:
                            no_answer_msg = (f"✅ No text answer was given by the model\n\n"
                                             f"Current Model Manager: `{model_manager_name}`\n"
                                             f"Current Model: `{model_name}`\nGenerated in {elapsed_time:.2f}s")
                            await quackamollie_bot.send_message(chat_id=message.chat.id,
                                                                reply_to_message_id=message.message_id,
                                                                text=no_answer_msg, parse_mode=ParseMode.MARKDOWN)
                        else:
                            clean_full_answer += (f"\n\nCurrent Model Manager: `{model_manager_name}`\n"
                                                  f"Current Model: `{model_name}`\nGenerated in {elapsed_time:.2f}s")
                            try:  # Try sending the answer as MARKDOWN
                                sent_message = await quackamollie_bot.send_message(
                                    chat_id=message.chat.id,
                                    text=clean_full_answer,
                                    reply_to_message_id=message.message_id,
                                    parse_mode=ParseMode.MARKDOWN)
                            except TelegramBadRequest:  # Send it as plain text if MARKDOWN formatting failed
                                sent_message = await quackamollie_bot.send_message(
                                    chat_id=message.chat.id,
                                    text=clean_full_answer,
                                    reply_to_message_id=message.message_id
                                )
                    # Else we edit the message sent with the full answer
                    else:
                        clean_full_answer += (f"\n\nCurrent Model Manager: `{model_manager_name}`\n"
                                              f"Current Model: `{model_name}`\nGenerated in {elapsed_time:.2f}s")
                        try:  # Try sending the answer as MARKDOWN
                            sent_message = await quackamollie_bot.edit_message_text(chat_id=message.chat.id,
                                                                                    message_id=sent_message.message_id,
                                                                                    text=clean_full_answer,
                                                                                    parse_mode=ParseMode.MARKDOWN)
                        except TelegramBadRequest:  # Send it as plain text if MARKDOWN formatting failed
                            sent_message = await quackamollie_bot.edit_message_text(chat_id=message.chat.id,
                                                                                    message_id=sent_message.message_id,
                                                                                    text=clean_full_answer)

                    # Save the answer generated by the model, if any, in the database
                    if clean_full_answer:
                        async with async_session() as session:
                            new_chat_answer = ChatMessage(id=sent_message.message_id, user_id=bot_id, chat_id=chat_id,
                                                          content=full_answer.strip(),
                                                          sent_at_datetime=sent_message.date.replace(tzinfo=None),
                                                          active=True)

                        async with session.begin():
                            session.add(new_chat_answer)

                    break  # Exit from the async loop when all done
        except TimeoutError:
            log.warning("A request was canceled due to a timeout error")
            await quackamollie_bot.send_message(chat_id=message.chat.id,
                                                text="❌ Unfortunately, your request was canceled due to"
                                                     " a timeout error",
                                                reply_to_message_id=message.message_id, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            error_msg = (f"An unhandled error occurred while answering with model manager `{model_manager_name}`"
                         f" and model `{model_name}` the prompt `{message.message_id}` of user `{user_id}`"
                         f" in chat `{chat_id}`\nTraceback:\n```\n{traceback.format_exc()}\n```")
            log.error(error_msg)
            await quackamollie_bot.send_message(chat_id=message.chat.id, text=error_msg,
                                                reply_to_message_id=message.message_id, parse_mode=ParseMode.MARKDOWN)
