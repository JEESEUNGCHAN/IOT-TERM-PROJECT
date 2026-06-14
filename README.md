# AIoT Smart Recycling System

**Introduction to Internet of Things (IoT) — Team Project**
Gachon University, School of Computing | Prof. Jaehyuk Choi | Spring 2026

---

## Overview

A low-cost, edge-AI recycling assistant built on **Raspberry Pi 4/5**.  
When a user approaches the bin, the system wakes, classifies the waste with **YOLOv8**, displays disposal instructions on an **LCD**, and automatically opens the correct bin lid via a **servo motor**.  
During standby, a **DHT22** sensor continuously tracks temperature and humidity for bin sanitation monitoring.

---

## System Architecture

```
User Approaches
      │
      ▼
Ultrasonic Sensor ──► Camera (YOLO Inference)
                              │
                              ▼
                    Waste Category Decision
                    ┌──────────────────────┐
                    │ plastic / can / paper │
                    │ glass / food / general│
                    └──────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         LCD Display     Servo Motor    Cloud Logger
        (Instructions)  (Open Lid)   (Google Sheets)
```

---

## Hardware

| Component | Purpose |
|-----------|---------|
| Raspberry Pi 4/5 | Edge computing hub |
| Pi Camera / USB Camera | YOLO image capture |
| HC-SR04 Ultrasonic | User proximity detection & fill-level |
| DHT22 | Temperature & humidity (sanitation) |
| I2C LCD 16×2 | Disposal instructions display |
| SG90 Servo × 6 | Automatic bin lid control |

### GPIO Wiring

| Sensor | Pin (BCM) |
|--------|-----------|
| Ultrasonic TRIG | 23 |
| Ultrasonic ECHO | 24 |
| DHT22 DATA | 4 |
| Servo (auto-lid) | 17 |
| LCD SDA | GPIO2 (I2C) |
| LCD SCL | GPIO3 (I2C) |

---

## Software Setup

```bash
# 1. Clone the repository
git clone https://github.com/JEESEUNGCHAN/IOT-TERM-PROJECT.git
cd IOT-TERM-PROJECT

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place YOLO model
cp /path/to/waste_yolov8n.pt models/

# 4. (Optional) Cloud logging — add credentials.json for Google Sheets
#    Set Telegram bot tokens for mobile notifications:
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# 5. Run
python main.py
```

---

## Module Structure

```
IOT-TERM-PROJECT/
├── main.py                  # System entry point & main loop
├── config.py                # GPIO pins, thresholds, waste info
├── requirements.txt
├── modules/
│   ├── ultrasonic.py        # Proximity & fill-level sensing
│   ├── dht_sensor.py        # Temperature/humidity monitoring
│   ├── lcd_display.py       # I2C LCD controller
│   ├── yolo_detector.py     # YOLOv8 waste classification
│   └── servo_control.py     # Automatic lid actuation
├── models/                  # YOLO model weights (.pt)
└── data/                    # Supplementary datasets
```

---

## Operational Flow

**Active Mode** (user present)
1. Ultrasonic sensor detects approach within 40 cm
2. Camera captures frame → YOLOv8 inference
3. Category voted across 3 frames for stability
4. LCD shows item name + disposal tip
5. Servo opens the matched bin lid for 5 seconds
6. Detection logged to CSV and Google Sheets

**Idle Mode** (no user)
1. DHT22 measures temperature & humidity every 30 seconds
2. LCD briefly shows environment status
3. If temp > 35°C or humidity > 80%, Telegram alert is sent

---

## Advanced Enhancements

| Feature | Description |
|---------|-------------|
| Auto-Lid Control | SG90 servo opens the correct bin automatically |

---

## Waste Categories

| Category | Bin Color | Disposal Tip |
|----------|-----------|--------------|
| Plastic | Blue | Remove cap & label |
| Can / Metal | Red | Rinse before dispose |
| Paper | Yellow | Keep dry & flat |
| Glass | Green | Wrap if broken |
| Food Waste | Brown | Drain liquid first |
| General | Grey | Non-recyclable |
