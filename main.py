# python3.6
#### ESPHome MQTT extractor
appver = "1.0.0"
appname = "EspHome MQTT extractor"
appshortname = "EMQTTEx"

import random
# import json
from paho.mqtt import client as mqtt_client
from prometheus_client import start_http_server, Gauge
from time import sleep as sleep
from datetime import datetime
from os import environ as environ

print(appname + " ver. "+appver)
# print('test_env_var:'+ str(test_env_var))
tab='  |'

env ='prod' #prod

if env == 'prod':
    server_port =int(environ.get('SERVER_PORT'))
    get_delay = int(environ.get('GET_DELAY'))
    broker = environ.get('BROKER_IP')
    port = int(environ.get('BROKER_PORT'))
    topic_pattern = environ.get('TOPIC')
    username = environ.get('USERNAME')
    password = environ.get('PASSWORD')
else:
    server_port=int('8081')
    get_delay = 10
    broker = 'ha.tomkat.cc'
    port = 1883
    topic_pattern = "esphome/meteo1/sensor/#"
    # topic_pattern = "tele/meteo1/sensor/meteo1_bme280-pressure/state"
    username = 'mqtt'
    password = 'mqtt001'

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

# metric_name=topic.replace('/','_')
# MQTT_VALUE = Gauge( topic_pattern.replace('/','_'), 'topic', ['topic','key','value','type'])
MQTT_VALUE = Gauge('esphome_sensor_state', 'topic', ['topic','value'])
APP_INFO = Gauge('app_info', 'Return app info',['appname','appshortname','version'])
APP_INFO.labels(appname,appshortname,appver).set(1)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        topic_name = msg.topic
        topic_name = topic_name.replace("/","_")
        topic_name = topic_name.replace("-", "_")
        value = msg.payload.decode()
        set_metrica(topic_name,value)

    client.subscribe(topic_pattern)
    client.on_message = on_message

def set_metrica(k,v):
    try:
        v = float(v)
        MQTT_VALUE.labels(k, 0).set(v)
    except  ValueError as e:
        print(e)
        MQTT_VALUE.labels(k, v).set(1)

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    try:
        start_http_server(server_port)
    except Exception as e: print(e)
    while True:
        run()
        sleep(get_delay)
