# PySensorMQTT/sensors/manager.py

import time
from PySensorMQTT.sensors.temperature import TemperatureSensor
from PySensorMQTT.sensors.humidity_air import HumidityAirSensor
from PySensorMQTT.sensors.humidity_soil import HumiditySoilSensor
from PySensorMQTT.sensors.light import LightSensor
from PySensorMQTT.sensors.motion import MotionSensor
from PySensorMQTT.sensors.modulo_rele import ModuloRele
from PySensorMQTT.sensors.base import MqttParameters

class SensorManager:
    """Gerenciador de sensores"""
    def __init__(self) -> None:
        """Inicializa o gerenciador de sensores.

        Cria uma lista vazia para armazenar os sensores.
        """
        self.sensors = []

    def add_sensor(self, parameters: MqttParameters) -> None:
        """Adiciona um sensor ao gerenciador

        Parameters:
            parameters (MqttParameters): Parâmetros do sensor

        Raises:
            ValueError: Se o tipo de sensor for inválido

        """
        sensor_classes = {
            'temperature': TemperatureSensor,
            'humidity_air': HumidityAirSensor,
            'humidity_soil': HumiditySoilSensor,
            'light': LightSensor,
            'motion': MotionSensor,
            'modulo_rele': ModuloRele,
            # Adicionar outros sensores
        }

        sensor_type = parameters.sensor_type
        if sensor_type not in sensor_classes:
            raise ValueError(f"Tipo de sensor inválido: {sensor_type}")

        sensor = sensor_classes[sensor_type](parameters)
        self.sensors.append(sensor)

    def start(self) -> None:
        """
        Inicia a execução dos sensores, publicando os dados em
        intervalos regulares.

        A execução é interrompida quando o usuário pressiona Ctrl+C.

        """
        try:
            while True:
                for sensor in self.sensors:
                    try:
                        sensor.publish()  # Publica os dados de cada sensor
                    except Exception as e:
                        print(f"Erro ao publicar no sensor {sensor.parameters.sensor_type}: {e}")
                # Aguarda pelo menor intervalo de atualização
                time.sleep(min(sensor.parameters.update_interval for sensor in self.sensors))
        except KeyboardInterrupt:
            # Garantir que os sensores se desconectem corretamente ao encerrar
            self.stop()

    def stop(self) -> None:
        # Método para parar e desconectar todos os sensores
        """
        Para todos os sensores, desconecta e para a execu o dos mesmos.

        Isso é util quando o programa precisa ser interrompido antes do
        tempo de execu o estimado.

        """
        for sensor in self.sensors:
            try:
                sensor.disconnect()  # Desconecta o sensor
                print(f"Sensor {sensor.parameters.sensor_type} desconectado.")
            except Exception as e:
                print(f"Erro ao desconectar o sensor {sensor.parameters.sensor_type}: {e}")
