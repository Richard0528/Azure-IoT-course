from base64 import b64encode, b64decode
from hashlib import sha256
from urllib import quote_plus, urlencode
from hmac import HMAC
import requests
import json
import time
from grovepi import *
 
## DHT sensor info
dht_sensor_port = 7 # connect the DHt sensor to port 7
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor
## BONUS: If you want to get the sound data, you need to declare the port here

## Azure IoT Hub connection
## The first connection string--primary key in week4
########## Task 1 -- Modify this part
URI = 'YOUR_IOT_HUB_NAME.azure-devices.net'
KEY = 'YOUR_IOT_HUB_PRIMARY_KEY'
IOT_DEVICE_ID = 'YOUR_IOT_DEVICE_ID'
POLICY = 'iothubowner'

## This code is based on an existing microsoft example(see below)
## Generate shared access signature toke for our Raspberry Pi
## You can learn more from the link below
## https://docs.microsoft.com/en-us/rest/api/eventhub/generate-sas-token
## Don't modify this following function
def generate_sas_token():
    expiry = 3600
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

## get the temperature and Humidity from the DHT sensor
## get the sound level from the sound sensor
## BONUS: If you want to add sound sensor, you may need to change this method
def read_temp():
    ## [temp, hum] contains two outputs from DHT sensor
    [ temp,hum ] = dht(dht_sensor_port, 0)
    return temp, hum

## Use the URI(Rest API) to send a message using JSON format
def send_message(token, message):
    ## The Rest API endpoint of Azure IoT hub
    url = 'https://{0}/devices/{1}/messages/events?api-version=2016-11-14'.format(URI, IOT_DEVICE_ID)
    ## Construct a header, use Json format as the content type
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    data = json.dumps(message)
    print(data)
    response = requests.post(url, data=data, headers=headers)

if __name__ == '__main__':

    ## Generate SAS Token
    token = generate_sas_token()

    ## Send Temperature to IoT Hub
    while True:
        temp, hum = read_temp()
        ########## Task 2 -- Modify the message
        ## Now the message only contains information of temperature
        ## Can you include humidity within the message as well?
        ## The message is in JSON format
        ## Read more information from this link: https://www.w3schools.com/js/js_json_syntax.asp
        ## Use "humidity" as the name of data
        ## BONUS: If you want to add sound data, use 'sound' as the name of data
        message = { "temp": str(temp) }
        send_message(token, message)
        time.sleep(5)




        