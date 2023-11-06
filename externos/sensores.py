import paho.mqtt.client as mqtt
import random
import time
import logging

import sys
sys.path.append(r'..')
from mqtt.auth import MQTTAuth

# Configuração do logger
logging.basicConfig(filename='../logs/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mqtt_broker_address = "localhost"  
mqtt_broker_port = 1883
mqtt_topic = "sensores"
mqtt_username = "user" 
mqtt_password = MQTTAuth().token().decode()


CLIENT = mqtt.Client()
CLIENT.username_pw_set(mqtt_username, mqtt_password) 
CLIENT.connect(mqtt_broker_address, mqtt_broker_port)

def publica_valor(valores):
    payload = f"{valores}"
    CLIENT.publish(mqtt_topic, payload)
    logging.info(f"[SENSORES] Valores publicados no tópico {mqtt_topic}: {payload}")

def validaValor():
    valor = random.randint(0, 50)
    if(valor >= 38):
        return None
    else:
        return valor

def geraValores():
    valores = [validaValor() for _ in range(4)]
    publica_valor(valores)

while True:
    geraValores()
    time.sleep(60)
