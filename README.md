# AIoT Smart Recycling System

**Introduction to Internet of Things (IoT) — Team Project**
Gachon University, School of Computing | Prof. Jaehyuk Choi | Spring 2026

---

## Overview

A low-cost, edge-AI recycling assistant built on **Raspberry Pi 5**.  
When a user approaches the bin, the system wakes, classifies the waste with **YOLOv8**, displays disposal instructions on an **LCD**, and automatically opens the bin lid via a **servo motor**.  
During standby, a **SHT30** sensor continuously tracks temperature and humidity for bin sanitation monitoring.

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
                    ┌─────────────────────┐
                    │ plastic / can / paper│
                    └─────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          LCD Display               Servo Motor
         (Instructions)             (Open Lid)
```

---

## Hardware

| Component | Purpose |
|-----------|---------|
| Raspberry Pi 5 | Edge computing hub |
| Pi Camera / USB Camera | YOLO image capture |
| HC-SR04 Ultrasonic | User proximity detection |
| SHT30 | Temperature & humidity (sanitation) |
| I2C LCD 16×2 | Disposal instructions display |
| SG90 Servo × 1 | Automatic bin lid control |

### GPIO Wiring

| Sensor | Pin (BCM) |
|--------|-----------|
| Ultrasonic TRIG | 14 |
| Ultrasonic ECHO | 15 |
| Servo (auto-lid) | 17 |
| LCD SDA | GPIO 2 (I2C) |
| LCD SCL | GPIO 3 (I2C) |
| SHT30 SDA | GPIO 2 (I2C, LCD와 공유) |
| SHT30 SCL | GPIO 3 (I2C, LCD와 공유) |

> **주의**: 초음파 ECHO 핀은 5V 출력 → GPIO 24에 직접 연결 금지.
> 1kΩ + 2kΩ 분압 저항 사용 필수.

---

## Software Setup

```bash
# 1. lgpio 시스템 패키지 설치 (RPi 5 필수)
sudo apt install -y python3-lgpio lgpio

# 2. 코드 받기
git clone https://github.com/JEESEUNGCHAN/IOT-TERM-PROJECT.git
cd IOT-TERM-PROJECT

# 3. Python 패키지 설치
pip install -r requirements.txt

# 4. I2C LCD 주소 확인 (0x27 이어야 함)
sudo i2cdetect -y 1

# 5. 실행
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
│   ├── dht_sensor.py        # Temperature/humidity (SHT30)
│   ├── lcd_display.py       # I2C LCD controller
│   ├── mqtt_client.py       # MQTT Publisher client
│   └── servo_control.py     # Automatic lid actuation (SG90)
│   ├── ultrasonic.py        # Proximity sensing (HC-SR04)
│   ├── yolo_detector.py     # YOLOv8 waste classification
├── models/                  # YOLO model weights (.pt)
└── data/                    # Supplementary datasets
```

---

## Operational Flow

**Active Mode** (user present)
1. Ultrasonic sensor detects approach within 40 cm
2. Camera captures frame → YOLOv8 inference (3-frame vote)
3. LCD shows item name + disposal tip
4. Send inference data via MQTT
5. Servo opens bin lid for 5 seconds then closes

**Idle Mode** (no user)
1. DHT22 measures temperature & humidity every 30 seconds
2. Send environmental data via MQTT
3. LCD briefly shows environment status

---

## Advanced Enhancements

| Feature | Description |
|---------|-------------|
| Auto-Lid Control | SG90 servo opens the bin lid automatically upon detection |
| Data sharing via MQTT | Shared via MQTT and can be monitored on a web dashboard |
| Multi-Frame Voting | Improving result reliability by analyzing multiple images |
| Broader Waste Detection | Enabled the detection of various recyclable and non-recyclable materials. |

---

## Waste Categories

| Category | Disposal Tip |
|----------|--------------|
| Plastic | Remove cap & label |
| Glass | Handle with care |
| Can / Metal | Rinse before dispose |
| Paper | Keep dry & flat |
| General Waste | Non-recyclable waste |
