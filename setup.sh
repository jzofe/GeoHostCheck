#!/bin/bash

clear

echo "Setup started..."

sudo apt-get install nodejs

sudo pacman -S nodejs

sudo npm install cfonts

sudo pip3 install -r requirements.txt

echo "Done! 'python3 geohc.py' "
