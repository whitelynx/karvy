#!/bin/bash

set -xe
exec &>$HOME/karvy-session.log

cd "$(dirname "$0")"

# Disable screen blanking
xset s off
xset -dpms
xset s noblank

# Start PulseAudio
pulseaudio --start

# Start DBus and session
touch ~/karvy-running
dbus-launch --exit-with-session bash -c "while [ -e ~/karvy-running ]; do python karvy.py; done; ratpoison -c quit"
