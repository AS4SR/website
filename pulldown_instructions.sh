#!/bin/bash
# Copyright 2017-2018 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/AS4SR/website
# Additional copyright may be held by others, as reflected in the commit history.
cd /home/wwwase/spacerobotics
mkdir -p git_pulls
cd git_pulls
rm master
rm -rf website-master
wget https://github.com/AS4SR/website/archive/master.zip
unzip master
cd website-master
chmod +x create_html.py
rm -rf /home/wwwase/spacerobotics/public_html
./create_html.py http://www.ase.uc.edu/~spacerobotics/ /home/wwwase/spacerobotics/git_pulls/website-master/ /home/wwwase/spacerobotics/public_html/
#cd /home/spacerobotics
##cp -R public_html public_html_old
##cd public_html
##rm -rf /home/spacerobotics/public_html/*
#rm -rf public_html
#cp -R /home/spacerobotics/git_pulls/website-master/public_html public_html
