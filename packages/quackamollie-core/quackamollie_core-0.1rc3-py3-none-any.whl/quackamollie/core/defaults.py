# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]


# Quackamollie CLI defaults
DEFAULT_CONFIG_FILE: str | None = None  #: Default configuration file path
DEFAULT_LOG_DIR: str | None = None  #: Default logging directory
DEFAULT_VERBOSITY: int = 0  #: Default verbosity level


# Quackamollie serve defaults
DEFAULT_OLLAMA_BASE_URL: str = "http://localhost:11434"
DEFAULT_MODEL_MANAGER: str | None = None
DEFAULT_MODEL: str | None = None
DEFAULT_DATA_DIR: str | None = "data/quackamollie"
DEFAULT_DB_PROTOCOL: str = "postgresql+asyncpg"
DEFAULT_DB_HOST: str | None = "0.0.0.0"
DEFAULT_DB_NAME: str | None = "quackamollie"

# Time str format defaults
DEFAULT_DATETIME_FORMAT: str = "%Y.%m.%d-%H.%M.%S %z"

# Defaults of the UserFilterMiddleware in charge of filtering non-authorized users
DEFAULT_USER_FILTER_MIDDLEWARE_INTERVAL_LIMIT: int = 2  # in seconds
DEFAULT_USER_FILTER_MIDDLEWARE_COUNTER_LIMIT: int = 7  # in number of messages
DEFAULT_USER_FILTER_MIDDLEWARE_COUNTER_LOW_LIMIT: int = 3  # in number of messages

# Default reaction emojis
DEFAULT_READ_REACTION_EMOJI: str = "🤔"
DEFAULT_ANSWERED_REACTION_EMOJI: str = "👌"

# Default message
DEFAULT_HISTORY_MAX_LENGTH: int | None = 20
DEFAULT_MIN_NB_CHUNK_TO_SHOW: int = 10
