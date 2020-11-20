#!/usr/bin/env bash

mkdir -p "/tmp"
PIDFILE="/tmp/nnysbot.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= |
                           grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
  echo "Already running."
  exit 99
fi

cd /root/nnysbot && /usr/bin/python3 main.py >> /root/cron.log &

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"