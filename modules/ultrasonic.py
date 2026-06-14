import time
import RPi.GPIO as GPIO
from config import ULTRASONIC_TRIG, ULTRASONIC_ECHO


class UltrasonicSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ULTRASONIC_TRIG, GPIO.OUT)
        GPIO.setup(ULTRASONIC_ECHO, GPIO.IN)
        GPIO.output(ULTRASONIC_TRIG, False)
        time.sleep(0.5)

    def measure_cm(self) -> float:
        GPIO.output(ULTRASONIC_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(ULTRASONIC_TRIG, False)

        start = time.time()
        while GPIO.input(ULTRASONIC_ECHO) == 0:
            start = time.time()

        stop = time.time()
        while GPIO.input(ULTRASONIC_ECHO) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = (elapsed * 34300) / 2
        return round(distance, 2)

    def is_object_present(self, threshold_cm: float) -> bool:
        return self.measure_cm() <= threshold_cm

    def get_fill_level_pct(self, bin_depth_cm: float = 40.0) -> int:
        dist = self.measure_cm()
        pct = max(0, min(100, int((1 - dist / bin_depth_cm) * 100)))
        return pct

    def cleanup(self):
        GPIO.cleanup()
