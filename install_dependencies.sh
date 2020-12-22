#!/bin/bash

python3 -c "import git"
if [ $? -ne 0 ]; then
	python3 -m pip install gitpython
else
	echo -e "\033[32mgitpython is installed\033[m"
fi 

python3 -c "import requests"
if [ $? -ne 0 ]; then
	python3 -m pip install requests
else
	echo -e "\033[32mrequests is installed\033[m"
fi

