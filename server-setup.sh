#!/bin/bash

SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 15 | head -n 1)
mkdir /"flag-folder-$SECRET"
mv /root/flag.txt /"flag-folder-$SECRET/flag.txt"
chmod 644 /"flag-folder-$SECRET/flag.txt"

runuser -l server-adm -c "cd /app/brokenide && python3 manage.py runserver 0.0.0.0:8000"
