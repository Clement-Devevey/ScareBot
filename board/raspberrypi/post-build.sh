#!/bin/sh

set -u
set -e
chmod 777 ${TARGET_DIR}/etc/init.d/S00gif
chmod 777 ${TARGET_DIR}/etc/init.d/S01game
rm -f ${TARGET_DIR}/etc/init.d/S01syslogd
rm -f ${TARGET_DIR}/etc/init.d/S02klogd
rm -f ${TARGET_DIR}/etc/init.d/S02sysctl
rm -f ${TARGET_DIR}/etc/init.d/S20urandom
rm -f ${TARGET_DIR}/etc/init.d/S40network
