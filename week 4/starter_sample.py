from iothub_client import IoTHubClient, IoTHubTransportProvider, IoTHubMessage
import time

CONNECTION_STRING = "HostName=testnumber2-hub.azure-devices.net;DeviceId=myRaspberryPi;SharedAccessKey=cw4WSWuwSCbbaBCrO2YRRj4z0rt+8SCRtJuD1yI6dxA="
PROTOCOL = IoTHubTransportProvider.MQTT

# output confirmation message
def send_confirmation_callback(message, result, user_context):
    print("Confirmation received for message with result = %s" % (result))

# main function
# send a message to the Auzre IoT hub
if __name__ == '__main__':
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    message = IoTHubMessage("test message")
    client.send_event_async(message, send_confirmation_callback, None)
    print("Message transmitted to IoT Hub")

    while True:
        time.sleep(1)