#!/bin/sh
# echo '*/5 * * * * run-server' > /etc/crontabs/root
# crond -l 2 -f

(crontab -l ; echo "*/5 * * * * /usr/src/app/scripts/runserver.sh >> /usr/src/app/logs/app.log") | crontab

touch /usr/src/app/logs/app.log
cron && tail -f /usr/src/app/logs/app.log