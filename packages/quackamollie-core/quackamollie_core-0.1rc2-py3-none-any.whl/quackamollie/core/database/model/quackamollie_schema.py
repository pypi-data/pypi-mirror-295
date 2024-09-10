# -*- coding: utf-8 -*-
""" Module containing all tables of the `quackamollie` postgresql database schema """
__all__ = ["User", "Chat", "ChatMember", "ChatSetting", "ChatMessage", "AppRole", "AppPermission",
           "ModelConfigPermission", "ModelConfig"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI", "NanaBanana"]

from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Relationship

from quackamollie.core.database.meta import TimeStampedModel
from quackamollie.core.enum.chat_type import ChatType
from quackamollie.core.enum.role_type import AppRoleType
from quackamollie.core.enum.user_type import UserType


class User(TimeStampedModel):
    """ Table listing users. It is autopopulated at startup by the CLI with the bot user and populated at runtime
        with Telegram users registering through the `/start` command.
    """
    __tablename__ = "users"
    __table_args__ = {'schema': 'quackamollie'}

    id = Column(BigInteger, primary_key=True)
    user_type = Column(postgresql.ENUM(UserType, schema="quackamollie_types"))
    app_role_id = Column(Integer, ForeignKey("quackamollie.app_roles.id"), nullable=False, index=True)
    full_name = Column(String(80), nullable=False)
    username = Column(String(80))
    first_name = Column(String(80))
    last_name = Column(String(80))

    app_role = Relationship("AppRole", back_populates="users")
    chats = Relationship("Chat", secondary="quackamollie.chat_members", back_populates="users")
    messages = Relationship("ChatMessage", back_populates="user")

    def __repr__(self):
        return (f"<{self.__class__.__name__}: id={self.id}, full_name='{self.full_name}', user_type='{self.user_type}',"
                f" app_role_id={self.app_role_id}>")


class Chat(TimeStampedModel):
    """ Table listing chats. It is populated at runtime with Telegram chats registered by users calling
        the `/start` command.
    """
    __tablename__ = "chats"
    __table_args__ = {'schema': 'quackamollie'}

    id = Column(BigInteger, primary_key=True)
    chat_name = Column(String(80), nullable=False)
    chat_type = Column(postgresql.ENUM(ChatType, schema="quackamollie_types"))

    users = Relationship("User", secondary="quackamollie.chat_members", back_populates="chats")
    settings = Relationship("ChatSetting", back_populates="chat", uselist=False, passive_deletes=True)
    messages = Relationship("ChatMessage", back_populates="chat", passive_deletes=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}: id={self.id}, chat_name='{self.chat_name}', chat_type='{self.chat_type}'>"


class ChatMember(TimeStampedModel):
    """ Join tables users and chats to handle many-to-many relationship """
    __tablename__ = "chat_members"
    __table_args__ = {'schema': 'quackamollie'}

    # user_id = Column(Integer, ForeignKey("quackamollie.users.id", ondelete="DELETE"), primary_key=True)
    user_id = Column(BigInteger, ForeignKey("quackamollie.users.id"), primary_key=True)
    # chat_id = Column(Integer, ForeignKey("quackamollie.chats.id", ondelete="DELETE"), primary_key=True)
    chat_id = Column(BigInteger, ForeignKey("quackamollie.chats.id"), primary_key=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}: user_id={self.user_id}, chat_id={self.chat_id}>"


class ChatSetting(TimeStampedModel):
    """ Table listing the settings of chats possibly changed at runtime by the users through the `/settings` command """
    __tablename__ = "chat_settings"
    __table_args__ = {'schema': 'quackamollie'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey("quackamollie.chats.id", ondelete="CASCADE"), nullable=False,
                     index=True, unique=True)
    chat_type_override = Column(postgresql.ENUM(ChatType, schema="quackamollie_types"), nullable=True)
    model_config_id = Column(Integer, ForeignKey("quackamollie.model_configs.id"), nullable=True, index=True)

    chat = Relationship("Chat", back_populates="settings")
    model_config = Relationship("ModelConfig")

    def __repr__(self):
        return (f"<{self.__class__.__name__}: chat_id={self.chat_id}, chat_type_override='{self.chat_type_override}',"
                f" model_config_id={self.model_config_id}>")


class ChatMessage(TimeStampedModel):
    """ Table listing messages sent by users through Telegram """
    __tablename__ = "chat_messages"
    __table_args__ = {'schema': 'quackamollie'}

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("quackamollie.users.id"), nullable=False, index=True)
    chat_id = Column(BigInteger, ForeignKey("quackamollie.chats.id", ondelete="CASCADE"), nullable=False,
                     index=True)  # , primary_key=True)
    content = Column(String(4096), nullable=False)
    sent_at_datetime = Column(DateTime, nullable=False, index=True)
    active = Column(Boolean, default=True, nullable=False)
    # files = Column(BLOB)
    # images = Column(BLOB)
    # sounds = Column(BLOB)

    user = Relationship("User", back_populates="messages")
    chat = Relationship("Chat", back_populates="messages")

    def __repr__(self):
        return (f"<{self.__class__.__name__}: user_id={self.user_id}, chat_id={self.chat_id}, content='{self.content}',"
                f" sent_at_datetime='{self.sent_at_datetime}', active={self.active}>")


class AppRole(TimeStampedModel):
    """ Table listing application roles determining rights of users to change global dynamic application settings """
    __tablename__ = "app_roles"
    __table_args__ = {'schema': 'quackamollie'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_type = Column(postgresql.ENUM(AppRoleType, schema="quackamollie_types"))

    users = Relationship("User", back_populates="app_role")
    permissions = Relationship("AppPermission", back_populates="role")

    def __repr__(self):
        return f"<{self.__class__.__name__}: id={self.id}, role_type='{self.role_type}'>"


class AppPermission(TimeStampedModel):
    """ Table listing application permissions determining rights to change global dynamic application settings
        depending on roles.
    """
    __tablename__ = "app_permissions"
    __table_args__ = {'schema': 'quackamollie'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("quackamollie.app_roles.id"), nullable=False, index=True)
    name = Column(String(80), nullable=False)
    type = Column(String(80), nullable=False)

    role = Relationship("AppRole", back_populates="permissions")

    __mapper_args__ = {
        "polymorphic_identity": "app_permissions",
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return (f"<{self.__class__.__name__}: id={self.id}, role_id={self.role_id}, name='{self.name}',"
                f" type='{self.type}'>")


class ModelConfigPermission(AppPermission):
    """ Table listing permissions specific to model config access depending on roles """
    __tablename__ = "model_config_permissions"
    __table_args__ = {'schema': 'quackamollie'}

    id = Column(Integer, ForeignKey("quackamollie.app_permissions.id", ondelete="CASCADE"), primary_key=True)
    model_config_id = Column(Integer, ForeignKey("quackamollie.model_configs.id"), nullable=False, index=True)
    read = Column(Boolean, default=False, nullable=False)
    write = Column(Boolean, default=False, nullable=False)
    delete = Column(Boolean, default=False, nullable=False)
    hidden = Column(Boolean, default=False, nullable=False)

    model_config = Relationship("ModelConfig", back_populates="permissions")

    __mapper_args__ = {
        "polymorphic_identity": "model_config_permissions",
    }

    def __repr__(self):
        return (f"<{self.__class__.__name__}: id={self.id}, role_id='{self.role_id}', name='{self.name}',"
                f" type='{self.type}', model_config_id={self.model_config_id}, read='{self.read}, write='{self.write},"
                f" delete='{self.delete}, hidden='{self.hidden}>")


class ModelConfig(TimeStampedModel):
    """ Table listing model configurations which are essentially a tuple of a model manager, a model name and
        an additional model configuration possibly null.
    """
    __tablename__ = "model_configs"
    __table_args__ = {'schema': 'quackamollie'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_name = Column(String(80), nullable=False)
    model_manager_type_id = Column(Integer, ForeignKey("quackamollie_types.model_manager_types.id"), nullable=False)
    model_name = Column(String(320), nullable=False)
    config = Column(String(1024), nullable=True)

    model_manager_type = Relationship("ModelManagerType", uselist=False)
    permissions = Relationship("ModelConfigPermission", back_populates="model_config")

    def __repr__(self):
        return (f"<{self.__class__.__name__}: id={self.id}, config_name={self.config_name},"
                f" model_manager_type_id={self.model_manager_type_id}, model_name='{self.model_name}',"
                f" config='{self.config}'>")
