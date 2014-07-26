#
# Regular cron jobs for the henkaru-traf-acct package
#
0 1 1 * *   root    find /opt/flow/ -type f -name 'ft*' -mtime +120 -delete 
0 2 1 * *   root    /opt/flow/bin/backup.sh 2>&1 >/dev/null
5 0 1 * *   root    /opt/flow/bin/report.py 2>&1 >/dev/null
