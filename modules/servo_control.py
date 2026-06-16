import time
import RPi.GPIO as GPIO
from config import SERVO_PIN

OPEN_DUTY  = 9.0   # ~90 degrees
CLOSE_DUTY = 6.0   # ~0 degrees
OPEN_SPEED = 0.5


class ServoController:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self._pwm = GPIO.PWM(SERVO_PIN, 50)
        self._pwm.start(CLOSE_DUTY)
        time.sleep(0.5)

    def open_lid(self, hold_sec: float = 5.0):
        pwm_state = CLOSE_DUTY
        while pwm_state < OPEN_DUTY:
            self._pwm.ChangeDutyCycle(pwm_state)
            pwm_state += OPEN_SPEED
            time.sleep(0.08)
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
