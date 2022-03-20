import json


def createMessage(lamp):
    if (lamp['on'] == True and lamp['online'] == True):
        state = "ON"
    else:
        state = "OFF"
    MQTT_MSG = json.dumps({
        "brightness": round(lamp['brightness'] / 100 * 255),
        "color": {
            "r": lamp['color']['r'],
            "g": lamp['color']['g'],
            "b": lamp['color']['b']
        },
        "state": state
    })
    return MQTT_MSG
