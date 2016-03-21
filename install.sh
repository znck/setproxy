#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

if [ -f setproxy.py ]
then
	cp setproxy.py /usr/local/bin/setproxy
else
    if type curl &>/dev/null
    then
        curl -O https://raw.githubusercontent.com/znck/setproxy/v0.0.1/setproxy.py
    else
        wget https://raw.githubusercontent.com/znck/setproxy/v0.0.1/setproxy.py
    fi
    if [ -f setproxy.py ]
    then
      cp setproxy.py /usr/local/bin/setproxy
    fi
fi
chmod +x /usr/local/bin/setproxy

if [ -f /usr/local/bin/setproxy ]
then
  echo Installation complete. Use command: setproxy
else
  echo Installation failed.
fi
