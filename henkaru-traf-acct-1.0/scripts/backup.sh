#!/bin/bash
# Backup and cleanup of traf table

begin=`date "+%F" -d "1 month ago"`
[ -d "/data/backups/traf-db" ] && mkdir -p /data/backups/traf-db || exit 1
mysqldump traf traf -w "timestamp" < $begin" | gzip -c > /data/backups/traf-db/traf.traf.`date +%F`.gz  
mysql traf -e "delete from traf where timestamp < $begin;"

exit 0
