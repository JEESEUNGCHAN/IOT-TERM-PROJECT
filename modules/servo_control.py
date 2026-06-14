import time
import RPi.GPIO as GPIO
from config import SERVO_PINS


OPEN_DUTY  = 7.5   # ~90 degrees
CLOSE_DUTY = 2.5   # ~0 degrees
MOVE_DELAY = 0.8


class ServoController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._pwm: dict = {}
        for category, pin in SERVO_PINS.items():
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, 50)
            pwm.start(CLOSE_DUTY)
            self._pwm[category] = pwm
        time.sleep(0.5)

    def open_lid(self, category: str, hold_sec: float = 5.0):
        if category not in self._pwm:
            return
        self._pwm[category].ChangeDutyCycle(OPEN_DUTY)
        time.sleep(MOVE_DELAY)
        self._pwm[category].ChangeDutyCycle(0)
        time.sleep(hold_sec)
        self._close_lid(category)

    def _close_lid(self, category: str):
        self._pwm[category].ChangeDutyCycle(CLOSE_DUTY)
        time.sleep(MOVE_DELAY)
        self._pwm[category].ChangeDutyCycle(0)

    def close_all(self):
        for category in self._pwm:
            self._close_lid(category)

    def cleanup(self):
        self.close_all()
        for pwm in self._pwm.values():
            pwm.stop()
        GPIO.cleanup()
