#!/bin/sh
#. /dockerfileGen/bin/activate
#nohup gunicorn -w 3 --bind unix:/run/ipc.sock wsgi:app &
/usr/sbin/nginx
