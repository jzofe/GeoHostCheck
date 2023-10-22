#!/bin/bash
 
clear
 
echo "Setup started..."
yes | sudo apt-get install python

clear 

yes | sudo apt-get install nodejs
 
clear
 
sudo pacman -S python --no-confirm
 
clear

sudo pacman -S nodejs --no-confirm

clear

sudo npm install cfonts
 
sudo pip3 install -r requirements.txt
 
echo "Done! 'python3 geohc.py' "
