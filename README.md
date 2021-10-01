# cnft-python
Cardano NFT Python


Clone the repository

    git clone https://github.com/larestrepo/cnft-python.git
    cd cnft-python




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


    git clone https://github.com/aws/aws-iot-device-sdk-python-v2.git
    python3 -m pip install ./aws-iot-device-sdk-python-v2

Make sure to have the following:

    sudo apt-get update
    sudo apt-get install cmake
    sudo apt-get install python3-dev


Use this file as example:

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

