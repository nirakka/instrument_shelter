import subprocess
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

host = 'hibernation.tech'
port = 1883
topic = 'rain'
GPIO.setmode(GPIO.BCM)


GPIO.setup(15, GPIO.IN)

def publish(data):
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(host, port=port, keepalive=60)

    client.publish(topic, data)

    client.disconnect()

subprocess.run(['raspistill', '-o', 'now.jpg'])
while True:
    subprocess.run(['mv', 'now.jpg', 'prev.jpg'])
    subprocess.run(['raspistill', '-o', 'now.jpg'])
    res = subprocess.run(['RainDetectionPrint','now.jpg','prev.jpg'], stdout=subprocess.PIPE)
    diff = res.stdout.decode()
    print(int(diff))
    print(GPIO.input(15))
    if int(diff) > 100000000 and GPIO.input(15) == 0:
        publish(1)
    else:
        publish(0)
