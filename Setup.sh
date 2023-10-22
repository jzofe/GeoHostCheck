#!/bin/bash
 
clear
 
echo "Setup started..."
yes | sudo apt-get install python
yes | sudo apt-get install nodejs
yes | sudo apt-get install npm
 
clear
 
sudo pacman -S python --no-confirm
sudo pacman -S nodejs --no-confirm
sudo pacman -S npm --no-confirm

clear

sudo npm install cfonts
 
sudo pip3 install -r requirements.txt
 
echo "Done! "

sudo python3 geohc.py
