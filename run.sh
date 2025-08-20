#!/bin/bash
set -e

echo "Installing dependencies..."
pip3 install -r requirements.txt --quiet --disable-pip-version-check

echo "Starting Pomodoro App..."
python3 main.py
