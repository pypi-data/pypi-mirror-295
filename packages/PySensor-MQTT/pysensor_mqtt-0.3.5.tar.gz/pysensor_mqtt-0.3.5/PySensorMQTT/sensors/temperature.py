# PySensorMQTT/sensors/temperature.py

import random
from datetime import datetime, timezone
from PySensorMQTT.sensors.base import SensorBase
import json

class TemperatureSensor(SensorBase):
    '''
    Classe para o sensor de temperatura
    '''
    def __init__(self, parameters):
        super().__init__(parameters)
        self.status = "ativo"  # Status inicial do sensor
        self.mqtt_client.subscribe(f"action/{self.parameters.sensor_type}", self.on_action_message)

    def generate_temperature(self) -> float:
        return round(random.uniform(15.0, 30.0), 2)

    def get_battery_level(self) -> int:
        # Simulando um nível de bateria aleatório entre 50% e 100%
        return random.randint(50, 100)

    def on_action_message(self, client, userdata, message):
        try:
            # Decodifica a mensagem de ação
            action_message = json.loads(message.payload.decode())
            device_id = action_message.get("device_id")
            action = action_message.get("action")

            # Verifica se a ação é para este dispositivo
            if device_id == self.parameters.device_id:
                if action == "off":
                    self.status = "desativado"
                    print(f"Dispositivo {self.parameters.device_id} desativado.")
                elif action == "on":
                    self.status = "ativo"
                    print(f"Dispositivo {self.parameters.device_id} ativado.")
        except Exception as e:
            print(f"Erro ao processar a mensagem de ação: {e}")

    def publish(self) -> None:
        try:
            # Obtendo o timestamp atual no formato ISO 8601 com timezone UTC
            timestamp = datetime.now(timezone.utc).isoformat()

            # Gerando o payload dependendo do status
            if self.status == "ativo":
                # Gerando o valor da temperatura
                temperature = self.generate_temperature()

                # Obtendo o nível de bateria
                battery_level = self.get_battery_level()

                # Criando o payload incluindo o device_id, unit, status, battery_level, e timestamp
                payload = {
                    "device_id": self.parameters.device_id,
                    "sensor_type": self.parameters.sensor_type,
                    "data": temperature,
                    "unit": "Celsius",
                    "status": self.status.upper(),
                    "battery_level": battery_level,
                    "timestamp": timestamp
                }
            else:
                # Se o dispositivo estiver desativado, enviar "-" no campo de data
                payload = {
                    "device_id": self.parameters.device_id,
                    "sensor_type": self.parameters.sensor_type,
                    "data": "-",
                    "unit": "Celsius",
                    "status": self.status.upper(),
                    "battery_level": "-",
                    "timestamp": timestamp
                }

            # Publicando a mensagem no broker
            self.mqtt_client.publish(self.parameters.topic, payload)
            print(f"Publicado com sucesso: {payload}")

        except Exception as e:
            # Tratando erros durante a geração ou publicação do payload
            print(f"Erro ao publicar o payload: {e}")
