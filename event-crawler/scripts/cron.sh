#!/bin/sh
# echo '*/5 * * * * run-server' > /etc/crontabs/root
# crond -l 2 -f

(crontab -l ; echo "*/15 * * * * /usr/src/app/scripts/runserver.sh >> /usr/src/app/logs/app.log") | crontab

touch /usr/src/app/logs/app.log
# to run crawler in startup (no need wait 15 minutes for first run)
nohup /usr/src/app/scripts/runserver.sh &
cron && tail -f /usr/src/app/logs/app.log