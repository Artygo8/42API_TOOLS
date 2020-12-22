#!/bin/bash

python3 -c "import git"
if [ $? -ne 0 ]; then
	echo -e "\033[35minstalling gitpython\033[m"
	python3 -m pip install gitpython
else
	echo -e "\033[32mgitpython is installed\033[m"
fi 

python3 -c "import requests"
if [ $? -ne 0 ]; then
	echo -e "\033[35minstalling requests\033[m"
	python3 -m pip install requests
else
	echo -e "\033[32mrequests is installed\033[m"
fi

python3 -c "import vlc"
if [ $? -ne 0 ]; then
	echo -e "\033[35minstalling vlc\033[m"
	python3 -m pip install python-vlc
else
	echo -e "\033[32mvlc is installed\033[m"
fi
