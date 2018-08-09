import paho.mqtt.client as mqtt
import subprocess
import datetime
import RPi.GPIO as GPIO
import pygame.mixer
import time
import schedule

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)

host = '192.168.1.9'
port = 1883
topic = 'rain'
flg = 0
def on_connect(client, userdata, flags, respons_code):
    #print('status {0}'.format(respons_code))
    client.subscribe(topic)

def reset_flg():
    global flg
    flg = 0
    #print("reset alarm!")

def on_message(client, userdata, msg):
    alarm  =  datetime.time(15,0,0)
    past_alarm = datetime.time(15, 30, 0)
    now = datetime.datetime.now().time()
    schedule.run_pending()
    if now > alarm and flg == 0 and now < past_alarm :
        rain = int(msg.payload.decode())
        if rain == 1 :
            global flg
            flg = 1

            pygame.mixer.init()
            pygame.mixer.music.load("alarm.mp3")
            pygame.mixer.music.play(-1)
            for i in range(240):
                value = GPIO.input(2)
                time.sleep(.2)
                if value == 1:
                    pygame.mixer.music.stop()
                    break

if __name__ == '__main__':
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    schedule.every().day.at("00:00").do(reset_flg)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port=port, keepalive=60)

    client.loop_forever()
