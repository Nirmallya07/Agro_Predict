import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "soil/npk"

def generate_realistic_npk():
    return {
        "N": random.randint(15, 60),
        "P": random.randint(10, 50),
        "K": random.randint(15, 60)
    }

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("MQTT Simulator Started...")

while True:
    data = generate_realistic_npk()
    client.publish(TOPIC, json.dumps(data))
    print("Published:", data)
    time.sleep(1)