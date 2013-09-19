#!/bin/sh

# Read configuration file (if its there)
if [ -s /boot/miner.conf ] ; then
    . /boot/miner.conf
fi

# "create" webpage from template
sed  '
s/@%@Pool_url@%@/'$url'/g
s/@%@Account@%@/'$account'/g
s/@%@Password@%@/'$password'/g' < /www/tmpl/miner_setting.html_tmpl > /www/pages/miner_setting.html
