#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

if [ -f setproxy.py ]
then
	cp setproxy.py /usr/bin/setproxy
else
    if type curl &>/dev/null
    then
        echo "" &>/dev/null
    else
        echo "Please install 'curl' to download setproxy."
        # apt-get install curl
        exit
    fi
	curl -sS https://raw.githubusercontent.com/znck/setproxy/master/setproxy.py >> /usr/bin/setproxy
fi
chmod +x /usr/bin/setproxy

echo Installation complete. Use command: setproxy
