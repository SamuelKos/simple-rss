#!/usr/bin/env bash

newdir=simplerss
if [[ -e ${newdir} ]]; then
 echo "install failure: directory ${newdir} already exist"
 exit 1
fi

apt -y install python3-tk python3-venv git && \
mkdir simplerss && \
cd simplerss && \
git clone https://github.com/SamuelKos/simple-rss . && \
./mkvenv env && \
echo "Installing done. Run with: ./reader.sh"

