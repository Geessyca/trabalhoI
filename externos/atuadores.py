import paho.mqtt.client as mqtt
import logging
import sys
sys.path.append(r'..')
from mqtt.auth import MQTTAuth
from middleware.auth import MiddlewareAuth

rpc=MiddlewareAuth()
conn = rpc.rpyc_connect('localhost', 18861, authorizer=rpc.token())
service = conn.root 


# Configuração do logger
logging.basicConfig(filename='../logs/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mqtt_broker_address = "localhost"
mqtt_broker_port = 1883
mqtt_pub_topic = "atuadores"
mqtt_sub_topic = "controlador"
mqtt_username = "user" 
mqtt_password = MQTTAuth().token().decode()

def on_connect(client, userdata, flags, rc):
    logging.info(f"[Atuador] - Conectado ao broker MQTT com resultado de código: {str(rc)}")
    client.subscribe(mqtt_sub_topic) 


def on_message(client, userdata, msg):
    logging.info(f"[Atuador] - Mensagem recebida no tópico {msg.topic}: {msg.payload.decode('utf-8')}")
    service.tratamentoAtuadores(msg.payload.decode('utf-8'))
    publica_valor(msg.payload)


client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password) 
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_address, mqtt_broker_port, 60)


def publica_valor(mensagem):
    client.publish(mqtt_pub_topic, mensagem)
    logging.info(f"[Atuadores] - Valores publicados no tópico {mqtt_pub_topic}: {mensagem}")

client.loop_forever()
