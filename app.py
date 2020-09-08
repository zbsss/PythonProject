from flask import Flask, render_template, url_for, request, redirect

from flask import Flask
from flask_mqtt import Mqtt

from reader import Reader, Device

reader = Reader('config.json')
rooms = reader.rooms
devices = reader.all_devices


app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = reader.broker
app.config['MQTT_USERNAME'] = reader.user
app.config['MQTT_PASSWORD'] = reader.password
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """
    Subscribes to all the topics from the config.json file.
    """
    for room in rooms.keys():
        mqtt.subscribe(room + "/#")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    """
    Logs all messages from subscribed topics to console.
    """
    topic = message.topic,
    payload = message.payload.decode()
    
    print("[INCOMING MESSAGE]", dict(
        topic=topic,
        payload=payload
    ))
    
    # Change device state when receiving message from server
    if topic in devices and payload in ['ON', 'OFF']:
        devices[topic].on = payload == 'ON'


@app.route('/')
def index():
    return render_template('layout.html', rooms=rooms)


@app.route('/<path:topic>')
def show_topic(topic):
    return render_template('layout.html', rooms=rooms, topic=topic)


@app.route('/switch/<path:topic>')
def switch(topic):
    device = devices[topic]
    device.toggle()
    mqtt.publish(topic, f"{'ON' if device.on else 'OFF'}")
    return render_template('layout.html', rooms=rooms, topic=device.parent_topic)


if __name__ == '__main__':
    app.run(debug=True)
