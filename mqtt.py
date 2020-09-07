import paho.mqtt.client as mqtt
import time
from reader import Reader

client = None


def on_log(client, userdata, level, buf):
    print("log:", buf)


def on_connect(clint, userdata, floags, rc):
    if rc == 0:
        print("connected: OK")
    else:
        print("connection FAILED: returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("disconnected: result code=", rc)


def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8"))
    print("message received:", m_decode, "on topic:", topic)


def main():
    """
    To start MQTT server run: net start mosquitto
    in folder: C:\Program Files\mosquitto
    OR:
        mosquitto.exe -c mosquitto.conf -v
    Adding a user and password:
        mosquitto_passwd.exe -c pwfile.example user
    My user: user: "user" password: "123"
    """
    reader = Reader("config.json")

    devices = reader.get_devices()
    broker = reader.broker

    for device in devices:
        print(device)
    print()

    print("Connecting to broker:", broker)
    client = mqtt.Client("python1")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_log = on_log

    client.username_pw_set(username="user", password="123")

    client.connect(broker)
    client.loop_start()

    # client.subscribe("house/speakers")
    client.subscribe("house/speakers/living-room")

    client.publish("house/speakers", "ON")
    client.publish("house/speakers/living-room", "OFF")

    time.sleep(4)

    client.loop_stop()
    client.disconnect()


if __name__ == '__main__':
    main()
