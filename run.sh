#!/usr/bin/env bash

mkdir -p "/tmp"
PIDFILE="/tmp/redditclipmirror.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= |
                           grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
  echo "Already running."
  exit 99
fi

cd /root/reddt-clip-mirror && /usr/bin/python3 main.py >> /root/reddt-clip-mirror/cron.log &

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"