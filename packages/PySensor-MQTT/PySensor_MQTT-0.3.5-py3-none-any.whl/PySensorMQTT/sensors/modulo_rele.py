# PySensorMQTT/sensors/modulo_rele.py

import random
from datetime import datetime, timezone
from PySensorMQTT.sensors.base import SensorBase
import json

class ModuloRele(SensorBase):
    '''
    Classe para simulador de um módulo relé (on/off)
    '''
    def __init__(self, parameters):
        super().__init__(parameters)
        self.status = "ativo"
        self.mqtt_client.subscribe(f"action/{self.parameters.sensor_type}", self.on_action_message)

    def get_relay_status(self) -> str:
        # Simula o status do módulo relé (on/off)
        return random.choice(["on", "off"])

    def get_battery_level(self) -> int:
        return random.randint(50, 100)

    def on_action_message(self, client, userdata, message):
        try:
            action_message = json.loads(message.payload.decode())
            device_id = action_message.get("device_id")
            action = action_message.get("action")

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
            if self.status == "ativo":
                relay_status = self.get_relay_status()
                battery_level = self.get_battery_level()

                payload = {
                    "device_id": self.parameters.device_id,
                    "sensor_type": self.parameters.sensor_type,
                    "data": relay_status,
                    "unit": "status",
                    "status": self.status.upper(),
                    "battery_level": battery_level,
                    "timestamp": timestamp
                }
            else:
                payload = {
                    "device_id": self.parameters.device_id,
                    "sensor_type": self.parameters.sensor_type,
                    "data": "-",
                    "unit": "status",
                    "status": self.status.upper(),
                    "battery_level": "-",
                    "timestamp": timestamp
                }

            self.mqtt_client.publish(self.parameters.topic, payload)
            print(f"Publicado com sucesso: {payload}")

        except Exception as e:
            print(f"Erro ao publicar o payload: {e}")
