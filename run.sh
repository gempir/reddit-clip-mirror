#!/usr/bin/env bash

mkdir -p "/tmp"
PIDFILE="/tmp/***REMOVED***.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= |
                           grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
  echo "Already running."
  exit 99
fi

/usr/bin/python3 /root/***REMOVED***/main.py >> /root/cron.log &

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"