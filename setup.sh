#!/bin/bash

sudo apt-get update
yes | sudo apt-get upgrade

echo "Installing packages ............................................................"
echo "Installing package: python3-pip ......................"
yes | sudo apt-get install python3-pip
echo "Installing package: speechrecognition ......................"
yes | sudo pip3 install speechrecognition
echo "Installing package: portaudio19-dev ......................"
yes | sudo apt-get install portaudio19-dev
echo "Installing package: pyttsx3 ......................"
yes | sudo pip3 install pyttsx3
echo "Installing package: pyaudio ......................"
yes | sudo pip3 install pyaudio
echo "Installing package: libsdl-ttf2.0-0 ......................"
yes | sudo apt-get install libsdl-ttf2.0-0
echo "Installing package: libsdl-mixer1.2 ......................"
yes | sudo apt-get install libsdl-mixer1.2
echo "Installing package: flac ......................"
yes | sudo apt-get install flac
echo "Installing package: pygame ......................"
yes | sudo pip3 install pygame
echo "Installing package: beautifulsoup4 ......................"
yes | sudo pip3 install beautifulsoup4
echo "Installing package: lxml ......................"
yes | sudo pip3 install lxml
echo "Installing package: googletrans ......................"
yes | sudo pip3 install googletrans
echo "Installing package: wikipedia ......................"
yes | sudo pip3 install wikipedia
echo "Installing package: spidev ......................"
yes | sudo pip3 install spidev
echo "Installing package: tkinter ......................"
yes | sudo pip3 install tkinter
echo "Installing package: transformers ......................"
yes | sudo pip3 install transformers
echo "Installing package: pandas ......................"
yes | sudo pip3 install pandas
echo "Installing package: torch ......................"
yes | sudo pip3 install torch
echo "Installing package: request ......................"
yes | sudo pip3 install request
echo "Installing package: datetime ......................"
yes | sudo pip3 install datetime
echo "Installing package: accelerate ......................"
yes | sudo pip3 install accelerate[torch]

echo "Installing sound card: seeed ....................."
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh  --compat-kernel