import logging
import paho.mqtt.client as mqtt


mqtt_broker_address = "localhost"  
mqtt_broker_port = 1883
mqtt_topic_sensores = "sensores"  
mqtt_topic_atuadores = "atuadores"  
mqtt_topic_controladores = "controladores"

logging.basicConfig(filename='sensores.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com resultado de código: " + str(rc))
    client.subscribe(mqtt_topic_sensores)

def atuadores():
    client.publish(mqtt_topic_atuadores, str("Ação"))

def controladores(message):
    client.publish(mqtt_topic_controladores, message)
    atuadores()

def on_message(client, userdata, msg):
    global sensor_values
    message=str(msg.payload)
    logging.info(message)
    controladores(message)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(mqtt_broker_address, mqtt_broker_port, 60)


client.loop_forever()
