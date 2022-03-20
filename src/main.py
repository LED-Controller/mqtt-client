import paho.mqtt.client as mqtt
import json
import time
import random

# Define Variables
from Rest import getlamps, updatelamps, authenticate
from createMessage import createMessage
from createconfig import createlamps
from processresponse import processresponse

MQTT_HOST = "192.168.178.57"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 0
MQTT_TOPIC = "homeassistant/light/"
CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'

USERNAME_MQTT = "mqtt-user"
PASSWORD_MQTT = "test"


def process_mac(mac):
    return mac.replace(':', '')


def on_connect(client, userdate, flags, rc):
    print("mqtt-Brocker mit status Code " + str(rc) + " verbunden")


def on_message(client, userdata, message):
    k = -1
    for i in range(len(lamps)):
        if process_mac(lamps[i]['mac']) in str(message.topic):
            k = i
            break
    payload = json.loads(message.payload.decode("utf8"))
    updatedlamp = processresponse(payload, lamps[k])
    # update change
    updatelamps(header, lamps[k])
    print("[" + str(lamps[k]['mac']) + "] wurde verändert: " + str(payload))
    MQTT_MSG = createMessage(updatedlamp)
    client.publish(MQTT_TOPIC + process_mac(updatedlamp['mac']) + "/state", MQTT_MSG)


# setup connection
client = mqtt.Client(CLIENT_ID)
client.username_pw_set(USERNAME_MQTT, PASSWORD_MQTT)
client.on_connect = on_connect
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

# authorize on backend
header = authenticate()
# initial get lamps
lamps = getlamps(header)
createlamps(client, lamps)
print("Lampen wurden initial vom Backend geladen")

for lamp in lamps:
    # recive message
    client.subscribe("homeassistant/light/" + process_mac(lamp['mac']) + "/set")
    client.on_message = on_message

# check for changes loop
frequency = 1
k = 0

while True:
    #Reduce the load during inactivity
    if k > 1000:
        frequency = 10
    if k > 50000:
        k = 1001
    new_lamps = getlamps(header)
    if lamps != new_lamps:
        k = 1
        frequency = 1
        lamps = new_lamps
        createlamps(client, lamps)
        for lamp in lamps:
            # recive message
            client.subscribe("homeassistant/light/" + process_mac(lamp['mac']) + "/set")
            client.on_message = on_message
    for lamp in lamps:
        # publish message
        MQTT_MSG = createMessage(lamp)
        client.publish(MQTT_TOPIC + process_mac(lamp['mac']) + "/state", MQTT_MSG)
    # print("Just published " + str(MQTT_MSG) + " to topic " + MQTT_TOPIC + lamp['mac'] + "/state")
    k = k + 1
    time.sleep(frequency)
