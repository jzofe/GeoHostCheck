#!/bin/bash
 
clear
 
echo "Setup started..."
pip3 install python-cfonts
 
sudo pip3 install -r requirements.txt
 
echo "Done! "

sudo python3 geohc.py
