# PySensorMQTT/sensors/base.py
from abc import ABC, abstractmethod
from typing import TypedDict
from PySensorMQTT.mqtt_sensor import MqttClient

class MqttParameters:
    def __init__(self, broker, port, topic, update_interval, sensor_type, device_id=None):
        """
        Inicializa os parâmetros do sensor.

        :param broker: Endere o do broker MQTT
        :param port: N mero da porta do broker MQTT
        :param topic: T pico MQTT para publica o do sensor
        :param update_interval: Intervalo de atualiza o do sensor em segundos
        :param sensor_type: Tipo do sensor
        :param device_id: Identificador nico do dispositivo (opcional)
        """
        self.broker = broker
        self.port = port
        self.topic = topic
        self.update_interval = update_interval
        self.sensor_type = sensor_type
        self.device_id = device_id  # Adicionando o campo device_id

class SensorBase(ABC):
    '''
    A classe SensorBase é uma classe base abstrata que fornece uma base para classes de sensores. 
    Ele inicializa um sensor com determinados parâmetros e configura uma conexão de cliente MQTT.
    '''

    parameters: MqttParameters
    def __init__(self, parameters: MqttParameters) -> None:
        """
        Inicializa o sensor com os parâmetros fornecidos.

        :param parameters: Parâmetros do sensor
        :type parameters: MqttParameters
        """
        self.parameters = parameters
        self.mqtt_client = MqttClient(parameters.broker, parameters.port)
        self.mqtt_client.connect()

    @abstractmethod
    def publish(self) -> None:
        
        """
        Publica a mensagem no t pico MQTT.

        Esta classe abstrata, portanto, as subclasses devem implementar este m todo.
        """
        
        raise NotImplementedError("Subclasses devem implementar este método.")

    # Método para desconectar o sensor
    def disconnect(self) -> None:
        
        """
        Desconecta o sensor do broker MQTT.

        Este método chamado quando o sensor precisa ser desativado.
        """
        self.mqtt_client.client.loop_stop()
        self.mqtt_client.client.disconnect()
