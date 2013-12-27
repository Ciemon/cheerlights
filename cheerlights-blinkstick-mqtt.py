#!/usr/bin/env python
# This is a for from https://bitbucket.org/thiseldo/random-python-code/src/8d5d0c7c17b9/Blinkstick/

from blinkstick import blinkstick
import sys
import mosquitto

def on_connect(mosq, obj, rc):
    print("rc: "+str(rc))

def on_message(mosq, obj, msg):
    sticks[0].set_color(name=(msg.payload))
    print(msg.topic+" "+str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)


def main():
    global sticks

    print "BlinkStick MQTT script"
    print ""

    sticks = blinkstick.find_all()
    if len(sticks) == 0:
        print "BlinkStick not found..."
        return 64

    mqttc = mosquitto.Mosquitto()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.connect("test.mosquitto.org", 1883, 60)
    mqttc.subscribe("cheerlights", 0)

    rc = 0
    while rc == 0:
        rc = mqttc.loop()

    return 0

if __name__ == "__main__":
    sys.exit(main())

