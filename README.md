# cnft-python

Cardano NFT Python
##

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

    pip3 install -r requirements.txt

However aws-iot-device-sdk-python-v2 should be installed manually

    sudo sudo apt update
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

#

### AWS IoT basic setup

Steps to configure basic communication (subscribe and connect)

In AWS account: 

1. Create a thing
2. Create certificates and attach to thing
3. Create policyID and attach to the certificates

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:<your specific end_point>:client/${iot:Connection.Thing.ThingName}"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Publish",
      "Resource": "arn:aws:<your specific end_point>:topic/sensor/data"
    }
  ]
}
```
4. Upload certificates to the remote "sensor" (Private and public keys, and root CA certificates Starfield Root CA Certificate) 

Ref: https://docs.aws.amazon.com/iot/latest/developerguide/server-authentication.html?icmpid=docs_iot_console#server-authentication-certs

5. (Optional) Start the app (AWS-thing.py) 

If you subscribe in AWS IoT, you should be see a return message similar to: 

```json
{
  "deviceid": "1",
  "datatime": "2021-09-24 10:48:41",
  "temperature": "11",
  "humidity": "90",
  "windDirection": "5",
  "windIntensity": "28",
  "rainHeight": "23"
}
```

##

### AWS IoT with sdk-python-v2 setup

Use this file as reference:

https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/pubsub.py


#### In addition to the previous steps in the basic setup and to start the pubsub using the websocket option 

1. Configure IAM user to allow the use of websockets with the sdk according to this guideline:

 Ref: https://docs.aws.amazon.com/iot/latest/developerguide/device-advisor-setting-up.html

2. Create the files in ~/.aws/credentials and ~/.aws/config

#### credentials:

    [default]
    aws_access_key_id=AKIAIOSFODNN7EXAMPLE
    aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

#### config

    [default]
    region=us-west-2
    output=json

Ref: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html

3. (Optional) In AWS CloudShell you could do:

    aws configure

And follow the steps from the shell. 

4. Create additional folders to contain certificates and secrets

It is needed cert, key and root-ca files. (Similar to Point 4 of the AWS basic setup)





