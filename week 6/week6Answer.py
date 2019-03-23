from base64 import b64encode, b64decode
from hashlib import sha256
from urllib import quote_plus, urlencode
from hmac import HMAC
import requests
import json
import os
import time
from grovepi import *
 

dht_sensor_port = 7 # connect the DHt sensor to port 7
sound_sensor = 2 # connect the sound sensor to port 2
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor


## Azure IoT Hub connection
URI = 'testnumber2-hub.azure-devices.net'
KEY = 'FZDgB1gD4Et/zUc7ExTCUdsxoNAO39IECxXc2KobOyU='
IOT_DEVICE_ID = 'myRaspberryPi'
POLICY = 'iothubowner'

## Generate shared access signature toke for our Raspberry Pi
## You can learn more from the link below
## https://docs.microsoft.com/en-us/rest/api/eventhub/generate-sas-token
def generate_sas_token():
    expiry=3600
    ttl = time.time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(URI)), int(ttl))
    signature = b64encode(HMAC(b64decode(KEY), sign_key, sha256).digest())

    rawtoken = {
        'sr' : URI,
        'sig': signature,
        'se' : str(int(ttl))
    }

    rawtoken['skn'] = POLICY

    return 'SharedAccessSignature ' + urlencode(rawtoken)

def read_temp():
    # get the temperature and Humidity from the DHT sensor
    # get the sound level from the sound sensor
    [ temp,hum ] = dht(dht_sensor_port, 0)
    sound = analogRead(sound_sensor)
    return temp, hum, sound

## Use the URI(Rest API) to send a message using JSON format
def send_message(token, message):
    url = 'https://{0}/devices/{1}/messages/events?api-version=2016-11-14'.format(URI, IOT_DEVICE_ID)
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    data = json.dumps(message)
    print(data)
    response = requests.post(url, data=data, headers=headers)

if __name__ == '__main__':

    # 1. Generate SAS Token
    token = generate_sas_token()

    # 2. Send Temperature to IoT Hub
    while True:
        temp, hum, sound = read_temp() 
        message = { "temp": str(temp), "humidity": str(hum), "sound": str(sound) }
        send_message(token, message)
        time.sleep(5)




