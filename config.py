# GPIO Pin Configuration
ULTRASONIC_TRIG = 14
ULTRASONIC_ECHO = 15
SERVO_PIN       = 17    # single servo for auto-lid demo
# SHT30 uses I2C (GPIO 2/3) shared with LCD — no extra pin needed

# System Thresholds
PROXIMITY_THRESHOLD_CM = 40
IDLE_MEASURE_INTERVAL  = 30

# YOLO
MODEL_PATH   = "models/waste_yolov8n.pt"
CONFIDENCE   = 0.3
FRAME_WIDTH  = 640
FRAME_HEIGHT = 480
CAMERA_INDEX = 1

# LCD (I2C)
LCD_I2C_ADDRESS = 0x27
LCD_ROWS        = 2
LCD_COLS        = 16

# Waste categories → disposal instructions
WASTE_INFO = {
    "plastic": {
        "label": "PLASTIC",
        "tip": "Remove cap & label",
    },
    "glass": {
        "label": "GLASS",
        "tip": "Handle with care",
    },
    "can": {
        "label": "CAN / METAL",
        "tip": "Rinse before dispose",
    },
    "paper": {
        "label": "PAPER",
        "tip": "Keep dry & flat",
    },
    "general": {
        "label": "GENERAL",
        "tip": "Non-recyclable waste",
    },
}

# YOLO class name → category mapping
YOLO_CLASS_MAP = {
    "can":                "can",
    "pop tab":            "can",
    "plastic bottle":     "plastic",
    "plastic bag":        "plastic",
    "plastic bottle cap": "plastic",
    "glass bottle":       "glass",
    "cardboard":          "paper",
    "paper":              "paper",
    "drink carton":       "paper",
    "battery":            "general",
    "null":               "general",
}
