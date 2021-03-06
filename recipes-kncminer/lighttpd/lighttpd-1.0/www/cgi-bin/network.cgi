#!/bin/sh
. ./cgi_lib.cgi

dhcp=false
error=false
dnsservers=""

valid_ip()
{
    local  ip=$1
    local  stat=0

    if [ "`echo $ip | grep -E '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'`" = "$ip" ]; then
        OIFS=$IFS
        IFS='.'
	
	for octet in $ip ; do
	    if [ ! $octet -le 255 ] ; then
		stat=1
	    fi
	done
        IFS=$OIFS
    else
	stat=1
    fi
    return $stat
}

valid_hostname()
{
    local  hostname="$1"
    local  stat=1

    if [ -n "$hostname" ] && [ "`echo $hostname | grep -E '^[0-9a-zA-Z-]{1,63}$'`" = "$hostname" ]; then
	stat=0;
    fi
    return $stat
}

if [ -f /etc/hostname ] ; then
    current_hostname=`cat /etc/hostname`
else
    current_hostname=Jupiter-XXX
fi

IFS="&"
set -- $QUERY_STRING

> /tmp/network.conf.$$
for i in $@; do
    IFS="="
    set -- $i
    if [ "$1" = "dhcp" ] ; then
	echo $1=$2 >> /tmp/network.conf.$$
	dhcp=true
    elif [ "$1" = "hostname" ] ; then
	if [ "$2" != "" ] ; then
	    input_hostname=`urldecode $2`
	    if [ "`echo "$input_hostname" | grep '\\\'`" != "" ] ; then
		input_hostname=`echo "$input_hostname" | sed 's!\\\!\\\\\\\!g'`
	    fi
	    if [ "`echo "$input_hostname" | grep \&`" != "" ] ;then
		input_hostname=`echo "$input_hostname" | sed 's!\&!\\\&!g'`
	    fi
	    valid_hostname "$input_hostname"
	    if [ $? -eq 0 ] ; then
		echo $1="$input_hostname" >> /tmp/network.conf.$$
	    else
		echo "hostname=$current_hostname" >> /tmp/network.conf.$$
	    fi
	else
	    echo "hostname=$current_hostname" >> /tmp/network.conf.$$
	fi
    fi
done

IFS="&"
set -- $QUERY_STRING

if [ "$dhcp" = true ] ; then
    rm /config/network.conf
    mv /tmp/network.conf.$$ /config/network.conf

else
    > /tmp/network.conf.$$
    for i in $@; do 
	IFS="="
	set -- $i
	if [ "$1" = "dnsservers" ] ; then
	    IFS="+"
	    set -- $2
	    for j in $@; do
		if [ "$j" != "" ] ; then
		    valid_ip $j
		    if [ $? -eq 0 ] ; then
			if [ "$dnsservers" = "" ] ; then
			    dnsservers=${j}
			else
			    dnsservers="${j} ${dnsservers}"
			fi
		    fi
		fi
	    done
	    IFS="="
	elif [ "$1" = "hostname" ] ; then
	    if [ "$2" != "" ] ; then
		input_hostname=`urldecode $2`
		if [ "`echo "$input_hostname" | grep '\\\'`" != "" ] ; then
		    input_hostname=`echo "$input_hostname" | sed 's!\\\!\\\\\\\!g'`
		fi
		if [ "`echo "$input_hostname" | grep \&`" != "" ] ;then
		    input_hostname=`echo "$input_hostname" | sed 's!\&!\\\&!g'`
		fi
		valid_hostname "$input_hostname"
		if [ $? -eq 0 ] ; then
		    echo $1="$input_hostname" >> /tmp/network.conf.$$
		else
		    echo "hostname=$current_hostname" >> /tmp/network.conf.$$
		fi
	    else
		echo "hostname=$current_hostname" >> /tmp/network.conf.$$
	    fi
	elif [ "$2" = "" ] ; then
	    # error, all fields are mandatory
	    error=true
	    invalid_parameter=$1
	    break
	else
	    valid_ip $2
	    if [ $? -eq 0 ] ; then
		echo $1=$2 >> /tmp/network.conf.$$

		if [ "$1" = "gateway" ] ; then
		    gateway=$2
		fi
	    else
		error=true
		invalid_parameter=$1
		invalid_value=$2
		break
	    fi
	fi
    done

    if [ "$dnsservers" = "" ] ; then
	echo "dnsservers=\""$gateway\" >> /tmp/network.conf.$$
    else
	echo "dnsservers=\""$dnsservers\" >> /tmp/network.conf.$$
    fi

    if [ "$error" = "false" ] ; then
	mv /tmp/network.conf.$$ /config/network.conf
    else
	rm /tmp/network.conf.$$
    fi
fi

if [ "$error" = "false" ] ; then
    QUIET=true /etc/init.d/network.sh
    if [ "$current_hostname" != "$input_hostname" ] ; then
	/etc/init.d/avahi restart > /dev/null
    fi
fi

./get_network_conf.cgi

exit 0
