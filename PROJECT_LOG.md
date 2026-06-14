# Smart Recycling System - 프로젝트 로그

## 프로젝트 개요
- **저장소:** https://github.com/JEESEUNGCHAN/IOT-TERM-PROJECT
- **하드웨어:** Raspberry Pi 5
- **기능:** 초음파 감지 → YOLO 분류 → 서보 제어 → MQTT 전송 → Node-RED 대시보드

---

## 하드웨어 구성

| 부품 | 핀 |
|---|---|
| Ultrasonic TRIG | GPIO 14 |
| Ultrasonic ECHO | GPIO 15 |
| Servo | GPIO 17 |
| SHT31D (온습도) | I2C (SDA=GPIO2, SCL=GPIO3), 주소 `0x45` |
| LCD 16x2 | I2C (SDA=GPIO2, SCL=GPIO3), 주소 `0x27` |
| CSI 카메라 | 리본 케이블 |

---

## RPi5 초기 세팅

### 1. 시스템 업데이트 & 패키지 설치
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv python3-dev python3-smbus i2c-tools git
```

### 2. I2C 활성화
```bash
sudo raspi-config
# Interface Options → I2C → Yes → Finish
sudo reboot
```

### 3. I2C 확인
```bash
sudo i2cdetect -y 1
# 0x27 (LCD), 0x45 (SHT31D) 보여야 정상
```

### 4. 저장소 클론
```bash
cd ~
git clone https://github.com/JEESEUNGCHAN/IOT-TERM-PROJECT.git
cd IOT-TERM-PROJECT
```

### 5. 가상환경 생성 및 라이브러리 설치
```bash
python3 -m venv venv
source venv/bin/activate

pip install rpi-lgpio lgpio
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
pip install adafruit-blinka adafruit-circuitpython-sht31d
pip install smbus2 RPLCD opencv-python
pip install paho-mqtt
```

### 6. picamera2 설치 (CSI 카메라)
```bash
sudo apt install -y libcap-dev
pip install picamera2

# pip 버전 제거 후 시스템 버전으로 교체
pip uninstall picamera2 -y
sudo apt install -y python3-picamera2
sudo ln -sf /usr/lib/python3/dist-packages/picamera2 venv/lib/python3.13/site-packages/
sudo ln -s /usr/lib/python3/dist-packages/libcamera venv/lib/python3.13/site-packages/
```

### 7. RPi5 GPIO 호환성 설정
```bash
# adafruit-blinka 설치 시 구버전 RPi.GPIO가 덮어씌워지면
pip uninstall RPi.GPIO -y
pip install rpi-lgpio --force-reinstall
```

---

## 실행 방법

```bash
cd ~/IOT-TERM-PROJECT
source venv/bin/activate
sudo venv/bin/python main.py
```

---

## MQTT + Node-RED 설정

### 설치
```bash
# mosquitto (MQTT 브로커)
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Node-RED
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
sudo systemctl enable nodered
sudo systemctl start nodered
```

### Node-RED flow import
1. 브라우저에서 `http://iotproject.local:1880` 접속
2. 햄버거 메뉴 → `Import` → `nodered_flow.json` 선택
3. `Deploy` 클릭

### 대시보드 확인
- 같은 와이파이의 어느 기기에서든 접속 가능
```
http://iotproject.local:1880/ui
```

### MQTT 토픽
| 토픽 | 내용 |
|---|---|
| `recycling/detection` | 분류 결과 (종류, 신뢰도, 시간) |
| `recycling/environment` | 온습도, 위생 상태 |

---

## 코드 수정 내역

### config.py
- `CAMERA_INDEX = 1` (CSI 카메라)
- `CONFIDENCE = 0.3` (인식률 향상)
- SHT31D 주소 `0x45` 반영
- `YOLO_CLASS_MAP` 커스텀 모델 클래스에 맞게 업데이트

```python
YOLO_CLASS_MAP = {
    "can":                "can",
    "pop tab":            "can",
    "plastic bottle":     "plastic",
    "plastic bag":        "plastic",
    "plastic bottle cap": "plastic",
    "cardboard":          "paper",
    "paper":              "paper",
    "drink carton":       "paper",
}
```

### modules/dht_sensor.py
- SHT31D I2C 주소 `0x45`로 변경
```python
self._device = adafruit_sht31d.SHT31D(i2c, address=0x45)
```

### modules/yolo_detector.py
- `cv2.VideoCapture` → `picamera2` 로 교체 (CSI 카메라 지원)

### main.py
- 초음파 감지 후 **5초 대기** (손 제거 시간)
- YOLO 판별 후 **3초 대기** (서보 작동 전)
- MQTT 전송 추가

### modules/mqtt_client.py (신규)
- 분류 결과 및 온습도 MQTT 전송

---

## YOLO 커스텀 모델

### 모델 학습 (Google Colab)
```python
!pip install roboflow ultralytics

from roboflow import Roboflow
rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace("fyp-bfx3h").project("yolov8-trash-detections")
version = project.version(2)
dataset = version.download("yolov8")

from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(data=f"{dataset.location}/data.yaml", epochs=50, imgsz=640)

from google.colab import files
import shutil
shutil.copy("runs/detect/train/weights/best.pt", "waste_yolov8n.pt")
files.download("waste_yolov8n.pt")
```

### 모델 RPi5로 전송
```bash
# PC 터미널에서
scp ~/Downloads/waste_yolov8n.pt gachon@iotproject.local:~/IOT-TERM-PROJECT/models/
```

### 클래스 확인
```bash
python3 -c "from ultralytics import YOLO; m=YOLO('models/waste_yolov8n.pt'); print(m.names)"
```

---

## SSH 접속
```bash
ssh gachon@iotproject.local
# 비밀번호: gachon
```

---

## 트러블슈팅

| 오류 | 원인 | 해결 |
|---|---|---|
| `No module named 'board'` | adafruit-blinka 미설치 | `pip install adafruit-blinka` |
| `Cannot determine SOC peripheral base address` | RPi5에서 구버전 RPi.GPIO | `pip uninstall RPi.GPIO -y && pip install rpi-lgpio --force-reinstall` |
| `No I2C device at address: 0x44` | SHT31D 주소 불일치 | `address=0x45` 로 변경 |
| `No module named 'picamera2'` | 가상환경에 picamera2 없음 | 시스템 패키지 심링크 |
| `No space left on device` | SD카드 용량 부족 | CPU 버전 torch 먼저 설치 |
| `CAMERA_INDEX out of range` | CSI 카메라는 cv2로 못 씀 | picamera2로 교체 |
