import time
from RPLCD.i2c import CharLCD
from config import LCD_I2C_ADDRESS, LCD_ROWS, LCD_COLS


class LCDDisplay:
    def __init__(self):
        self._lcd = CharLCD(
            i2c_expander="PCF8574",
            address=LCD_I2C_ADDRESS,
            port=1,
            cols=LCD_COLS,
            rows=LCD_ROWS,
            dotsize=8,
        )
        self.clear()

    def clear(self):
        self._lcd.clear()

    def show(self, line1: str, line2: str = ""):
        self._lcd.clear()
        self._lcd.write_string(line1[:LCD_COLS])
        if line2 and LCD_ROWS >= 2:
            self._lcd.crlf()
            self._lcd.write_string(line2[:LCD_COLS])

    def show_detection(self, label: str, tip: str):
        self.show(f"Found:{label[:10]}", tip[:LCD_COLS])

    def show_environment(self, temp: float, hum: float):
        self.show(f"Temp: {temp:.1f}C", f"Hum:  {hum:.1f}%")

    def show_idle(self):
        self.show("SmartRecycle", "Ready...")

    def show_bin_full(self, category: str):
        self.show(f"{category[:8]} BIN FULL", "Call staff!")

    def scroll_message(self, message: str, delay: float = 0.4):
        padded = " " * LCD_COLS + message + " " * LCD_COLS
        for i in range(len(padded) - LCD_COLS + 1):
            self._lcd.clear()
            self._lcd.write_string(padded[i:i + LCD_COLS])
            time.sleep(delay)

    def cleanup(self):
        self.clear()
