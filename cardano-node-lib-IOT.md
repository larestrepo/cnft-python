### Cardano Node python library

If you want to use this library but don't have installed Cardano node or Cardano wallet, then you need to configure your server/interface as a client API. We are using IOT core to open a websocket subscription to allow communication with our infrastructure. Instructions below.

### Configure Virtual Environment for Python

    sudo apt update && upgrade -y

Command for python3

    sudo apt install python3-pip
    pip3 --version
    sudo -H pip3 install -upgrade pip
    sudo -H pip3 install virtualenv virtualenvwrapper

Setting up env variables for the virtual environment

    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
    echo "export WORKON_HOME=~/Env" >> ~/.bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
    source ~/.bashrc

Create the virtual environment

    mkvirtualenv <name of the virtual environment>

The virtual env wrapper should do all the work for you, install python inside and launch it.

Everytime you want to start the virtualenv just type: workon <name of the virtual environment>

Install aws-iot-device-sdk-python-v2

    sudo apt update
    sudo apt install cmake
    sudo apt install python3-dev

    cd ~/git

    git clone https://github.com/aws/aws-iot-device-sdk-python-v2.git
    python3 -m pip install ./aws-iot-device-sdk-python-v2



### Clone the repository

    cd ~/git
    git clone https://github.com/larestrepo/cnft-python.git
    cd cnft-python

With the virtual environment active:

    pip install -r requirements.txt

If requirements.txt still contains the aws-iot-device-sdk-python-v2 remove it, otherwise it will throw errors.


