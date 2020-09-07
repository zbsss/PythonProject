import json


class Device:
    def __init__(self, parent_topic, name, on=True):
        self.parent_topic = parent_topic
        self.topic = parent_topic + '/' + name
        self.name = name
        self.on = on

    def __repr__(self):
        return f"{self.topic}: {'ON' if self.on else 'OFF'}"

    def toggle(self):
        self.on = not self.on


class Reader:
    def __init__(self, filename):
        with open(filename) as f:
            data = json.load(f)

        self.broker = data['broker']
        self.user = data['user']
        self.password = data['password']

        self.rooms = {}
        self.all_devices = {}
        for room in data['rooms']:
            self.rooms[room['topic']] = [Device(room['topic'], device) for device in room['devices']]

        for room in self.rooms.values():
            for device in room:
                self.all_devices[device.topic] = device

