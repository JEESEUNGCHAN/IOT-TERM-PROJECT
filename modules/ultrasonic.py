import time
import RPi.GPIO as GPIO
from config import ULTRASONIC_TRIG, ULTRASONIC_ECHO

TIMEOUT = 0.04   # 40ms → ~6.8m max range


class UltrasonicSensor:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ULTRASONIC_TRIG, GPIO.OUT)
        GPIO.setup(ULTRASONIC_ECHO, GPIO.IN)
        GPIO.output(ULTRASONIC_TRIG, False)
        time.sleep(0.5)

    def measure_cm(self) -> float:
        GPIO.output(ULTRASONIC_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(ULTRASONIC_TRIG, False)

        deadline = time.time() + TIMEOUT
        start = time.time()
        while GPIO.input(ULTRASONIC_ECHO) == 0:
            start = time.time()
            if time.time() > deadline:
                return 999.0

        deadline = time.time() + TIMEOUT
        stop = time.time()
        while GPIO.input(ULTRASONIC_ECHO) == 1:
            stop = time.time()
            if time.time() > deadline:
                return 999.0

        distance = ((stop - start) * 34300) / 2
        return round(distance, 2)

    def is_object_present(self, threshold_cm: float) -> bool:
        return self.measure_cm() <= threshold_cm
