#!/bin/bash
 
clear
 
echo "Setup started..."

sudo apt-get install python3-tk
sudo pacman -S python3-tk 
pip3 install python-cfonts
 
sudo pip3 install -r requirements.txt
 
echo "Done! "

sudo python3 geohc.py
