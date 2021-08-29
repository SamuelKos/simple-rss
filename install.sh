#!/usr/bin/env bash

apt -y install python3-tk python3-venv && \
cd simple-rss && ./mkvenv env && \
echo "Installing done. Run with: ./reader.sh"

