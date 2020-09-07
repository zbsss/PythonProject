from flask import Flask, render_template, url_for, request, redirect

from flask import Flask
from flask_mqtt import Mqtt

from reader import Reader, Device

reader = Reader('config.json')
rooms = reader.rooms
broker = reader.broker

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = broker
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
    print(dict(
        topic=message.topic,
        payload=message.payload.decode()
    ))


@app.route('/')
def index():
    return render_template('layout.html', rooms=rooms)


@app.route('/<path:topic>')
def show_topic(topic):
    return render_template('layout.html', rooms=rooms, topic=topic)


@app.route('/toggle_device', methods=["GET", "POST"])
def toggle_device():
    if request.method == 'POST':
        print(request.base_url)
        turned_on = request.form.getlist('on')
        print(turned_on)
        return redirect(request.url)
    return render_template('layout.html', rooms=rooms)
    # reader.all_devices[device_topic].toggle()


if __name__ == '__main__':
    app.run(debug=True)