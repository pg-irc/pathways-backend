#!/usr/local/bin/bash

FILENAME=pathways-production-backup-`date +"%Y-%m-%d"`.psql-db-dump

heroku pg:backups:capture  --app=pathways-production
heroku pg:backups:download --app=pathways-production --output=$FILENAME

./manage.py reset_db
./manage.py migrate

pg_restore --verbose --clean --no-acl --no-owner -h localhost -U `whoami` -d pathways_local $FILENAME

echo
echo "To check backup content:"
echo "psql -d pathways_local"
echo "select * from push_notifications_pushnotificationtoken;"
echo "then upload $FILENAME to google drive"
