import cv2
import time
from ultralytics import YOLO
from config import MODEL_PATH, CONFIDENCE, FRAME_WIDTH, FRAME_HEIGHT, CAMERA_INDEX, YOLO_CLASS_MAP


class WasteDetector:
    def __init__(self):
        self._model  = YOLO(MODEL_PATH)
        self._cap    = cv2.VideoCapture(CAMERA_INDEX)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH,  FRAME_WIDTH)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    def _map_class(self, class_name: str) -> str:
        name = class_name.lower().strip()
        for key, category in YOLO_CLASS_MAP.items():
            if key in name:
                return category
        return "general"

    def capture_frame(self):
        ret, frame = self._cap.read()
        return frame if ret else None

    def detect(self) -> dict | None:
        frame = self.capture_frame()
        if frame is None:
            return None

        results = self._model(frame, conf=CONFIDENCE, verbose=False)

        best = None
        best_conf = 0.0
        for r in results:
            for box in r.boxes:
                conf  = float(box.conf[0])
                cls   = int(box.cls[0])
                label = self._model.names[cls]
                if conf > best_conf:
                    best_conf = conf
                    best = {
                        "raw_class": label,
                        "category":  self._map_class(label),
                        "confidence": round(conf, 3),
                        "timestamp":  time.strftime("%Y-%m-%d %H:%M:%S"),
                        "frame":      frame,
                    }
        return best

    def detect_stable(self, samples: int = 3, interval: float = 0.4) -> dict | None:
        votes: dict[str, int] = {}
        last: dict | None = None
        for _ in range(samples):
            result = self.detect()
            if result:
                cat = result["category"]
                votes[cat] = votes.get(cat, 0) + 1
                last = result
            time.sleep(interval)

        if not votes:
            return None

        best_cat = max(votes, key=votes.__getitem__)
        if last:
            last["category"] = best_cat
        return last

    def cleanup(self):
        self._cap.release()
