import time
import adafruit_dht
import board
from config import DHT_PIN


class DHTSensor:
    def __init__(self):
        pin_map = {
            4:  board.D4,
            17: board.D17,
            18: board.D18,
            27: board.D27,
        }
        self._device = adafruit_dht.DHT22(pin_map.get(DHT_PIN, board.D4))

    def read(self) -> dict:
        for _ in range(3):
            try:
                temp = self._device.temperature
                hum  = self._device.humidity
                if temp is not None and hum is not None:
                    return {
                        "temperature_c": round(temp, 1),
                        "humidity_pct":  round(hum, 1),
                        "timestamp":     time.strftime("%Y-%m-%d %H:%M:%S"),
                    }
            except RuntimeError:
                time.sleep(2)
        return {"temperature_c": None, "humidity_pct": None, "timestamp": None}

    def sanitation_status(self) -> str:
        data = self.read()
        if data["temperature_c"] is None:
            return "UNKNOWN"
        if data["temperature_c"] > 35 or data["humidity_pct"] > 80:
            return "WARNING"
        if data["temperature_c"] > 30 or data["humidity_pct"] > 70:
            return "CAUTION"
        return "NORMAL"

    def cleanup(self):
        self._device.exit()
