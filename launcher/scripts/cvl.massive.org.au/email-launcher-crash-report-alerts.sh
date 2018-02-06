#!/bin/bash

# This file, used by the Launcher, lives in
# /root/cron/email-launcher-crash-report-alerts.sh
# on cvl.massive.org.au
# Running crontab -l as root gives:
# */5 * * * * /root/cron/email-launcher-crash-report-alerts.sh

tmp=`mktemp`

find /opt/launcher_crash_reports/ -type f -mmin -5 | while read filename
do
    if [ ! -z "$(grep 'Contact me? Yes' $filename)" ]; then
        recipients="help@massive.org.au"
        sender=$( cat $filename | grep Email: | sed 's/Email://' )
        export REPLYTO="$sender"
        export EMAIL="$sender"
        config=$( cat $filename | grep 'DEBUG - Config' | sed 's/.*DEBUG - Config: //' )
        nametag=$(echo $sender | sed 's/@.*//')
        mutt -s "Strudel Debug Log: $nametag - $config " $recipients < $filename
        echo "$(date): Sent launcher crash report $sender $recipients $filename" >> email.log
    fi
done

rm -f $tmp
