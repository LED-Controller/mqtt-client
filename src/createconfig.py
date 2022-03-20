import json


def createlamps(client, lamps):
    for lamp in lamps:
        mac = lamp['mac'].replace(':', '')
        configuration_topic = "homeassistant/light/" + mac + "/config"
        configuration_payload = json.dumps({
            "~": "homeassistant/light/"+mac,
            "name": lamp['name'],
            "unique_id": mac,
            "cmd_t": "~/set",
            "stat_t": "~/state",
            "schema": "json",
            "brightness": "true",
            "rgb": "true"
        })
        client.publish(configuration_topic, configuration_payload)
