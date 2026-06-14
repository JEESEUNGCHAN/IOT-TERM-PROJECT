# GPIO Pin Configuration
ULTRASONIC_TRIG = 23
ULTRASONIC_ECHO = 24
DHT_PIN = 4
SERVO_PINS = {
    "plastic":    17,
    "can":        18,
    "paper":      27,
    "glass":      22,
    "food":       10,
    "general":    9,
}

# System Thresholds
PROXIMITY_THRESHOLD_CM = 40     # trigger distance for user detection
IDLE_MEASURE_INTERVAL  = 30     # seconds between DHT22 readings
BIN_FULL_THRESHOLD_CM  = 8      # ultrasonic fill-level alert

# YOLO
MODEL_PATH   = "models/waste_yolov8n.pt"
CONFIDENCE   = 0.45
FRAME_WIDTH  = 640
FRAME_HEIGHT = 480
CAMERA_INDEX = 0

# LCD (I2C)
LCD_I2C_ADDRESS = 0x27
LCD_ROWS        = 2
LCD_COLS        = 16

# Waste categories → disposal instructions
WASTE_INFO = {
    "plastic": {
        "label": "PLASTIC",
        "bin_color": "BLUE",
        "tip": "Remove cap & label",
    },
    "can": {
        "label": "CAN / METAL",
        "bin_color": "RED",
        "tip": "Rinse before dispose",
    },
    "paper": {
        "label": "PAPER",
        "bin_color": "YELLOW",
        "tip": "Keep dry & flat",
    },
    "glass": {
        "label": "GLASS",
        "bin_color": "GREEN",
        "tip": "Wrap if broken",
    },
    "food": {
        "label": "FOOD WASTE",
        "bin_color": "BROWN",
        "tip": "Drain liquid first",
    },
    "general": {
        "label": "GENERAL",
        "bin_color": "GREY",
        "tip": "Non-recyclable",
    },
}

# YOLO class name → internal category mapping
YOLO_CLASS_MAP = {
    "bottle":         "plastic",
    "pet bottle":     "plastic",
    "plastic bag":    "plastic",
    "can":            "can",
    "tin can":        "can",
    "aluminum can":   "can",
    "cardboard":      "paper",
    "newspaper":      "paper",
    "paper":          "paper",
    "glass bottle":   "glass",
    "glass":          "glass",
    "food":           "food",
    "banana peel":    "food",
    "styrofoam":      "general",
    "diaper":         "general",
}

# Cloud logging (Google Sheets)
GSHEET_CREDENTIALS = "credentials.json"
GSHEET_NAME        = "SmartRecycling_Log"
GSHEET_WORKSHEET   = "detections"
