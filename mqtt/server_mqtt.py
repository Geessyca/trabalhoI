import logging
import paho.mqtt.client as mqtt
import sys
sys.path.append(r'..')
from mqtt.auth import MQTTAuth
from middleware.auth import MiddlewareAuth

rpc=MiddlewareAuth()
conn = rpc.rpyc_connect('localhost', 18861, authorizer=rpc.token())
service = conn.root 


mqtt_broker_address = "localhost"
mqtt_broker_port = 1883
mqtt_topic_sensores = "sensores"
mqtt_topic_atuadores = "atuadores"
mqtt_topic_controlador = "controlador"
mqtt_username = "user" 
mqtt_password = MQTTAuth().token().decode()

logging.basicConfig(filename='../logs/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com resultado de código: " + str(rc))
    client.subscribe(mqtt_topic_sensores)
    client.subscribe(mqtt_topic_atuadores)
    client.subscribe(mqtt_topic_controlador)

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    if topic == mqtt_topic_sensores:
        message = service.save_sensor(payload)
        logging.info(f"[Sensores] = {payload}")
        client.publish(mqtt_topic_controlador, message)
    elif topic== mqtt_topic_atuadores:
        logging.info(f"[Atuadores] = {payload}")
    else:
        logging.info(f"[Controlador] = {payload}")
    


client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password) 
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_address, mqtt_broker_port, 60)

client.loop_forever()
