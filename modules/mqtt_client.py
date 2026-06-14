import json
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT   = 1883

TOPIC_DETECTION   = "recycling/detection"
TOPIC_ENVIRONMENT = "recycling/environment"


class MQTTClient:
    def __init__(self):
        self._client = mqtt.Client()
        try:
            self._client.connect(BROKER, PORT, keepalive=60)
            self._client.loop_start()
            print("[MQTT] Connected to broker.")
        except Exception as e:
            print(f"[MQTT] Connection failed: {e}")

    def publish_detection(self, category: str, label: str, confidence: float):
        payload = json.dumps({
            "category":   category,
            "label":      label,
            "confidence": round(confidence, 3),
            "timestamp":  time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        self._client.publish(TOPIC_DETECTION, payload)

    def publish_environment(self, temp: float, hum: float, status: str):
        payload = json.dumps({
            "temperature": temp,
            "humidity":    hum,
            "status":      status,
            "timestamp":   time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        self._client.publish(TOPIC_ENVIRONMENT, payload)

    def cleanup(self):
        self._client.loop_stop()
        self._client.disconnect()
