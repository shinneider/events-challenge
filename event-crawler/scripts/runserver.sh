#!/bin/sh
echo "STARTING"
cd /usr/src/app/
echo "  --installing requirements"
/usr/local/bin/pip install -r requirements.txt >> /usr/src/app/logs/app.log
echo "  --starting app"
/usr/local/bin/python main.py