import time
import board
import busio
import adafruit_sht31d


class DHTSensor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self._device = adafruit_sht31d.SHT31D(i2c, address=0x45)

    def read(self) -> dict:
        try:
            temp = round(self._device.temperature, 1)
            hum  = round(self._device.relative_humidity, 1)
            return {
                "temperature_c": temp,
                "humidity_pct":  hum,
                "timestamp":     time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        except Exception:
            return {"temperature_c": None, "humidity_pct": None, "timestamp": None}

    def sanitation_status(self, data: dict) -> str:
        if data["temperature_c"] is None:
            return "UNKNOWN"
        if data["temperature_c"] > 35 or data["humidity_pct"] > 80:
            return "WARNING"
        if data["temperature_c"] > 30 or data["humidity_pct"] > 70:
            return "CAUTION"
        return "NORMAL"

    def cleanup(self):
        pass
