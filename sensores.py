import paho.mqtt.client as mqtt
import random
import time

mqtt_broker_address = "localhost"  
mqtt_broker_port = 1883
mqtt_topic = "sensores"

CLIENT = mqtt.Client()
CLIENT.connect(mqtt_broker_address, mqtt_broker_port)


def publica_valor(posi,valores):
    payload = f"{posi}:{valores}"
    CLIENT.publish(mqtt_topic, payload)

def validaValor():
    valor = random.randint(0, 25)
    if(valor >= 18):
        return None
    else:
        return valor

def geraN():
    publica_valor("N",validaValor())

def geraS():
    publica_valor("S",validaValor())

def geraL():
    publica_valor("L",validaValor())

def geraO():
    publica_valor("O",validaValor())


while True:
    geraN()
    geraS()
    geraL()
    geraO()
    time.sleep(5)
