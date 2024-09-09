# PySensorMQTT/mqtt_sensor.py
import paho.mqtt.client as mqtt
import json  # Para decodificar as mensagens recebidas em formato JSON

class MqttClient:
    """Classe para o cliente MQTT."""
    def __init__(self, broker: str, port: int):
        """
        Inicializa o cliente MQTT com o broker e porta fornecidos.

        :param broker: Endere o do broker MQTT
        :param port: N mero da porta do broker MQTT
        """
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port

        # Definindo os callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log

    def connect(self) -> None:
        
        """
        Conecta ao broker MQTT e inicia o loop.

        :raises: Exce o caso n o seja poss vel conectar ao broker MQTT
        """
        try:
            # Conecta ao broker MQTT e inicia o loop
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
        except Exception as e:
            print(f"Erro ao conectar ao broker: {e}")
            raise

    # Callback para conexão
    def on_connect(self, client, userdata, flags, reason_code):
        if reason_code == 0:
            print("Conectado com sucesso ao broker!")
        else:
            print(f"Falha ao conectar ao broker. Código de razão: {reason_code}")

    # Callback para desconexão
    def on_disconnect(self, client, userdata, rc):
        print("Desconectado do broker.")

    # Callback para quando uma mensagem é publicada
    def on_publish(self, client, userdata, mid):
        print(f"Mensagem publicada com sucesso. ID da mensagem: {mid}")

    # Função para publicar mensagens
    def publish(self, topic: str, payload: dict) -> None:
        # Convertendo o payload para JSON
        payload_str = json.dumps(payload)
        self.client.publish(topic, payload_str)
        print(f"Publicado no tópico {topic}: {payload_str}")

    # Função para subscrever a um tópico
    def subscribe(self, topic: str, on_message_callback) -> None:
        # Função de callback chamada quando uma mensagem é recebida no tópico
        self.client.subscribe(topic)
        self.client.on_message = on_message_callback

    # Função de callback chamada ao receber uma mensagem
    def handle_message(self, client, userdata, msg):
        try:
            # Decodifica o payload e processa a mensagem recebida
            payload = json.loads(msg.payload.decode())
            print(f"Mensagem recebida no tópico {msg.topic}: {payload}")
        except Exception as e:
            print(f"Erro ao processar a mensagem: {e}")

    # Callback para registro de logs
    def on_log(self, client, userdata, level, buf):
        print(f"Log MQTT: {buf}")
