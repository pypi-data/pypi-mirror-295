import unittest
from PySensorMQTT.sensors.temperature import TemperatureSensor
from PySensorMQTT.sensors.base import MqttParameters

class TestTemperatureSensor(unittest.TestCase):
    def test_generate_temperature(self):
        parameters: MqttParameters = {
            'sensor_name': 'temp_sensor',
            'broker': 'localhost',
            'port': 1883,
            'topic': 'sensor/temperature',
            'update_interval': 5,
            'sensor_type': 'temperature'
        }
        sensor = TemperatureSensor(parameters)
        temperature = sensor.generate_temperature()
        self.assertIsInstance(temperature, float)