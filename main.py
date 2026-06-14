import time
import signal
import sys
import RPi.GPIO as GPIO

from config import (
    PROXIMITY_THRESHOLD_CM,
    IDLE_MEASURE_INTERVAL,
    WASTE_INFO,
)
from modules.ultrasonic    import UltrasonicSensor
from modules.dht_sensor    import DHTSensor
from modules.lcd_display   import LCDDisplay
from modules.yolo_detector import WasteDetector
from modules.servo_control import ServoController


class SmartRecyclingSystem:
    def __init__(self):
        print("[System] Initializing...")
        self.ultrasonic = UltrasonicSensor()
        self.dht        = DHTSensor()
        self.lcd        = LCDDisplay()
        self.detector   = WasteDetector()
        self.servo      = ServoController()

        self._last_env_time = 0.0
        self._running       = True

        signal.signal(signal.SIGINT,  self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)
        print("[System] Ready.")

    def run(self):
        self.lcd.show_idle()

        while self._running:
            now = time.time()
            if now - self._last_env_time >= IDLE_MEASURE_INTERVAL:
                self._monitor_environment()
                self._last_env_time = now

            distance = self.ultrasonic.measure_cm()
            if distance <= PROXIMITY_THRESHOLD_CM:
                self._handle_waste_event()

            time.sleep(0.2)

    def _handle_waste_event(self):
        self.lcd.show("Scanning...", "Hold item still")
        print("[Detection] Object detected, running YOLO...")

        result = self.detector.detect_stable(samples=3, interval=0.4)

        if result is None:
            self.lcd.show("No item found", "Try again")
            time.sleep(2)
            self.lcd.show_idle()
            return

        category = result["category"]
        info     = WASTE_INFO.get(category)

        if info is None:
            self.lcd.show("Unknown item", "Try again")
            time.sleep(2)
            self.lcd.show_idle()
            return

        print(f"[Detection] {info['label']} ({result['confidence']:.0%})")
        self.lcd.show_detection(info["label"], info["tip"])
        self.servo.open_lid(hold_sec=5.0)

        time.sleep(3)
        self.lcd.show_idle()

    def _monitor_environment(self):
        data   = self.dht.read()
        status = self.dht.sanitation_status(data)

        temp = data["temperature_c"]
        hum  = data["humidity_pct"]

        if temp is None:
            return

        print(f"[ENV] {temp}C  {hum}%  -> {status}")
        self.lcd.show_environment(temp, hum)
        time.sleep(3)
        self.lcd.show_idle()

    def _shutdown(self, *_):
        print("\n[System] Shutting down...")
        self._running = False
        self.lcd.show("Goodbye!", "")
        time.sleep(1)
        self.servo.cleanup()
        self.detector.cleanup()
        self.lcd.cleanup()
        self.dht.cleanup()
        GPIO.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    SmartRecyclingSystem().run()
