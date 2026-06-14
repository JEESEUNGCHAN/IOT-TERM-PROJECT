import time
import RPi.GPIO as GPIO
from config import SERVO_PIN

OPEN_DUTY  = 7.5   # ~90 degrees
CLOSE_DUTY = 2.5   # ~0 degrees


class ServoController:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self._pwm = GPIO.PWM(SERVO_PIN, 50)
        self._pwm.start(CLOSE_DUTY)
        time.sleep(0.5)

    def open_lid(self, hold_sec: float = 5.0):
        self._pwm.ChangeDutyCycle(OPEN_DUTY)
        time.sleep(0.8)
        self._pwm.ChangeDutyCycle(0)
        time.sleep(hold_sec)
        self._close_lid()

    def _close_lid(self):
        self._pwm.ChangeDutyCycle(CLOSE_DUTY)
        time.sleep(0.8)
        self._pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self._close_lid()
        self._pwm.stop()
