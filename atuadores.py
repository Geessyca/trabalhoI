import paho.mqtt.client as mqtt

mqtt_broker_address = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "atuadores"

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com resultado de código: {str(rc)}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode('utf-8')}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_address, mqtt_broker_port, 60)

client.loop_forever()
