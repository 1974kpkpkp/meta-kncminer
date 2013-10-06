#!/bin/sh

if [ -z "$QUERY_STRING" ] ; then
    show_same_page
    exit 0
fi
IFS="&"
set -- $QUERY_STRING

for i in $@; do 
    IFS="="
    set -- $i
    if [ "$1" = "ssh_on" ] && [ $2 -eq 1 ] ; then
	echo NO_START=1 > /config/dropbear
    else
	> /config/dropbear
    fi
done

/etc/init.d/dropbear stop > /dev/null
/etc/init.d/dropbear start > /dev/null

./get_services_conf.cgi

exit 0
