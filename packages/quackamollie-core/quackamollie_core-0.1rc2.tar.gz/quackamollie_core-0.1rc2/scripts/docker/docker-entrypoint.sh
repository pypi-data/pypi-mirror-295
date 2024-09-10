#!/bin/sh
set -e

user_id="${USER_ID:-942}"
group_id="${GROUP_ID:-942}"

getent group "${group_id}" > /dev/null || addgroup -S -g "${group_id}" quackamollie
getent passwd "${user_id}" > /dev/null || adduser -S -h "$(pwd)" -H -s /bin/sh -u "${user_id}" -G "$(getent group ${group_id} | cut -d: -f1)" quackamollie

mkdir -p "${QUACKAMOLLIE_DATA_DIR:-/quackamollie/data}"
chown -R "${user_id}:${group_id}" "${QUACKAMOLLIE_DATA_DIR:-/quackamollie/data}"

mkdir -p "${QUACKAMOLLIE_LOG_DIR:-/quackamollie/logs}"
chown -R "${user_id}:${group_id}" "${QUACKAMOLLIE_LOG_DIR:-/quackamollie/logs}"

exec su -l "$(getent passwd ${user_id} | cut -d: -f1)" -c "$*"
