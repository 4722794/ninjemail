#!bash

pip install -r requirements.txt
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install -f
sudo dpkg -i google-chrome-stable_current_amd64.deb
python emailcreator.py