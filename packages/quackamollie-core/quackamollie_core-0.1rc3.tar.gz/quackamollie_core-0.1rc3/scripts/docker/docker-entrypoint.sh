#!/bin/sh
set -e

user_id="${USER_ID:-942}"
group_id="${GROUP_ID:-942}"

# Create group and user from environment variables or default
getent group "${group_id}" > /dev/null || addgroup -S -g "${group_id}" quackamollie
getent passwd "${user_id}" > /dev/null || adduser -S -h "$(pwd)" -H -s /bin/sh -u "${user_id}" -G "$(getent group ${group_id} | cut -d: -f1)" quackamollie

# Create the data directory if it doesn't exist and set its owner to the specified user from USER_ID
mkdir -p "${QUACKAMOLLIE_DATA_DIR:-/quackamollie/data}"
chown -R "${user_id}:${group_id}" "${QUACKAMOLLIE_DATA_DIR:-/quackamollie/data}"

# If `QUACKAMOLLIE_LOG_DIR` environment variable is defined, create the log directory and set its owner to the specified user from USER_ID
if [ -n "${QUACKAMOLLIE_LOG_DIR:-}" ]; then
  mkdir -p "${QUACKAMOLLIE_LOG_DIR}";
  chown -R "${user_id}:${group_id}" "${QUACKAMOLLIE_LOG_DIR}";
fi

# Format all environment variables names as a list separated by commas for `runuser`'s `--whitelist-environment` option
quackamollie_env_var_names="$(env | awk -F "=" '/QUACKAMOLLIE_/{printf "%s%s", sep, $1; sep=","}')"
if [ "${DEBUG:-}" = "true" ] || [ "${DEBUG:-}" = "True" ] || [ "${DEBUG:-}" = "TRUE" ]; then
  echo "DEBUG - quackamollie_env_var_names='${quackamollie_env_var_names}'";
fi

# Run given command as specified user from USER_ID (so we're not running quackamollie as root)
exec runuser -u "$(getent passwd ${user_id} | cut -d: -f1)" --whitelist-environment "${quackamollie_env_var_names}" -- "$@"
