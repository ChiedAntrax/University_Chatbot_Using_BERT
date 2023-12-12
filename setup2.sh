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
yes | sudo apt-get install python3-pyaudio
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
yes | sudo apt-get install python3-lxml
echo "Installing package: googletrans ......................"
yes | sudo pip3 install googletrans
echo "Installing package: wikipedia ......................"
yes | sudo pip3 install wikipedia
echo "Installing package: spidev ......................"
yes | sudo pip3 install spidev
echo "Installing package: tkinter ......................"
yes | sudo apt-get install python3-tk
echo "Installing package: transformers ......................"
yes | sudo pip3 install transformers
echo "Installing package: pandas ......................"
yes | sudo pip3 install pandas
echo "Installing package: torch ......................"
yes | sudo pip3 install torch
echo "Installing package: requests ......................"
yes | sudo pip3 install requests
echo "Installing package: datetime ......................"
yes | sudo pip3 install datetime
echo "Installing package: accelerate ......................"
yes | sudo pip3 install accelerate[torch]

echo "Installing sound card: seeed ....................."
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh --compat-kernel

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install \
    accelerate==0.25.0 \
    certifi==2023.11.17 \
    charset-normalizer==3.3.2 \
    click==8.1.7 \
    colorama==0.4.6 \
    comtypes==1.2.0 \
    filelock==3.13.1 \
    fsspec==2023.12.1 \
    gTTS==2.4.0 \
    huggingface-hub==0.19.4 \
    idna==3.6 \
    Jinja2==3.1.2 \
    joblib==1.3.2 \
    MarkupSafe==2.1.3 \
    mpmath==1.3.0 \
    networkx==3.2.1 \
    numpy==1.26.2 \
    packaging==23.2 \
    pandas==2.1.3 \
    psutil==5.9.6 \
    pygame==2.5.2 \
    pypiwin32==223 \
    python-dateutil==2.8.2 \
    pyttsx3==2.90 \
    pytz==2023.3.post1 \
    pywin32==306 \
    PyYAML==6.0.1 \
    regex==2023.10.3 \
    requests==2.31.0 \
    safetensors==0.4.1 \
    scikit-learn==1.3.2 \
    scipy==1.11.4 \
    six==1.16.0 \
    SpeechRecognition==3.10.1 \
    sympy==1.12 \
    threadpoolctl==3.2.0 \
    tk==0.1.0 \
    tokenizers==0.15.0 \
    torch==2.1.1 \
    tqdm==4.66.1 \
    transformers==4.35.2 \
    typing_extensions==4.8.0 \
    tzdata==2023.3 \
    urllib3==2.1.0

# Deactivate the virtual environment
deactivate

echo "Setup complete. Activate the virtual environment using 'source venv/bin/activate'."
