import time
import json
from machine import I2C, Pin, reset
from wifi import wifiConnect
from mqtt import MQTTClient
from bmp180 import BMP180
import dht
from mqtt import MQTTClient

# Das initialisierung von WLAN und Topic welches auf dem MQTT Broker angezeigt wird
ssid = "my-ssid"
password = "my-password"
topic = b'my/topic'

# MQTT Broker auswÃ¤hlen und definieren
MQTT_BROKER = "test.mosquitto.org"

# MQTT Broker initialisieren
client = MQTTClient(MQTT_BROKER, keepalive=60)

# Sensoren Initialisieren
i2c = I2C(scl=Pin(5), sda=Pin(4))
bmp = BMP180(i2c, 100100.0)
sensor = dht.DHT22(Pin(2))


# Definieren von der Hauptfunktion
def connect():
    conNet()
    conMQTT()


# Das Verbinden des MQTT Brokers
def conMQTT():
    print("Connecting to MQTT server... ", end="")

    try:
        client.mqttConnect()
    except OSError as e:
        print('Failed to connect to MQTT broker.')
        print('Reconnecting...')
        time.sleep(10)
        conMQTT()


# Das Verbinden mit der WLAN
def conNet():
    print("Connecting to WiFi", end="")
    try:
        wifiConnect(ssid, password)
    except OSError as e:
        print('Failed to connect to Local Network.')
        print('Reconnecting...')
        time.sleep(10)
        conNet()


# Die Hauptfunktion aufrufen
connect()

# Das Messen der Messwerte und das Senden an den MQTT Broker in json format
while True:
    print("Measuring height and weather conditions... ", end="")
    try:
        sensor.measure()
    except OSError as e:
        reset()
    messwerte = {
        "pressure": bmp.pressure/100.0,
        "humidity": sensor.humidity(),
        "temperature": bmp.temperature,
        "altitude": bmp.altitude,
    }

    print(messwerte)
    try:
        client.mqttPublish(topic, json.dumps(messwerte))
    except OSError as e:
        print('Disconnected from Broker, reconnecting...', e)
        conMQTT()
    time.sleep(5)