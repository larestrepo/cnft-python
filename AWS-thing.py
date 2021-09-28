import paho.mqtt.client as mqtt
import ssl
from time import sleep
from random import randint
import json
import datetime

connflag = False

def on_connect(client, suerdata, flags, rc):
    global connflag
    print('Connection to AWS')
    connflag = True
    print('Connection returned result :' +  str(rc))

mqttc = mqtt.Client('Raspbey_thing')
mqttc.on_connect = on_connect

awshost = 'a1rgstrntakbmi-ats.iot.us-east-2.amazonaws.com'
awsport = 8883
caPath = './certificates/AmazonRootCA1.pem'
certPath = './certificates/2beae4c39f-certificate.pem.crt'
keyPath = './certificates/2beae4c39f-private.pem.key'

mqttc.tls_set(ca_certs=caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED,
              tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  

mqttc.connect (awshost, awsport, keepalive = 60)

mqttc.loop_start()

while True:
    sleep(5)
    if connflag == True:
        temp = str(randint(-50,50))
        hum = str(randint(0,100))
        wind_dir = str(randint(0,360))
        wind_int = str(randint(0,100))
        rain = str(randint(0,50))
        time = str(datetime.datetime.now())[:19]

        data = {'deviceid':str(1), 'datatime':time, 'temperature':temp, 'humidity':hum,
                'windDirection':wind_dir, 'windIntensity':wind_int, 'rainHeight':rain}
        jsonData = json.dumps(data)
        mqttc.publish('sensor/data', jsonData, qos = 1) # Publish the data as json with the topic: sensor/data

        print('Meesage sent: time ', time)
        print('Meesage sent: temperature ', temp, " Celsius")
        print('Meesage sent: humidity ', hum, ' %')
        print('Meesage sent: windDirection ', wind_dir, " Degrees")
        print('Meesage sent: windIntensity ', wind_int, ' m/s')
        print('Meesage sent: rainHeight ', rain, ' mm/h\n')
    else:
        print('waiting for connection...')