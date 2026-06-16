import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import paho.mqtt.client as mqtt

latest = {
    "detection":   {"label": "-", "confidence": 0, "category": "-", "timestamp": "-"},
    "environment": {"temperature": "-", "humidity": "-", "status": "-", "timestamp": "-"},
}

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        if msg.topic == "recycling/detection":
            latest["detection"] = data
        elif msg.topic == "recycling/environment":
            latest["environment"] = data
    except Exception:
        pass

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)
mqtt_client.subscribe([("recycling/detection", 0), ("recycling/environment", 0)])
mqtt_client.loop_start()

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="3">
<title>Smart Recycling Dashboard</title>
<style>
  body {{ font-family: sans-serif; background: #f4f4f4; padding: 24px; margin: 0; }}
  h1   {{ color: #333; }}
  h2   {{ color: #555; margin: 24px 0 12px; }}
  .row {{ display: flex; flex-wrap: wrap; gap: 16px; }}
  .card {{ background: #fff; border-radius: 10px; padding: 20px 28px;
           box-shadow: 0 2px 6px rgba(0,0,0,.12); min-width: 160px; }}
  .label {{ font-size: 13px; color: #888; margin-bottom: 6px; }}
  .value {{ font-size: 34px; font-weight: bold; color: #0094CE; }}
  .NORMAL  {{ color: #2ecc40; }}
  .CAUTION {{ color: #ff851b; }}
  .WARNING {{ color: #ff4136; }}
  .ts {{ margin-top: 28px; color: #aaa; font-size: 12px; }}
</style>
</head>
<body>
<h1>Smart Recycling Dashboard</h1>

<h2>Detection</h2>
<div class="row">
  <div class="card"><div class="label">Detected Item</div><div class="value">{label}</div></div>
  <div class="card"><div class="label">Confidence</div><div class="value">{confidence}%</div></div>
  <div class="card"><div class="label">Category</div><div class="value">{category}</div></div>
</div>

<h2>Environment</h2>
<div class="row">
  <div class="card"><div class="label">Temperature</div><div class="value">{temp}°C</div></div>
  <div class="card"><div class="label">Humidity</div><div class="value">{hum}%</div></div>
  <div class="card"><div class="label">Sanitation Status</div>
    <div class="value {status}">{status}</div></div>
</div>

<p class="ts">Auto-refresh every 3s &nbsp;|&nbsp; Last update: {ts}</p>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        d = latest["detection"]
        e = latest["environment"]
        conf = d.get("confidence", 0)
        if isinstance(conf, float) and conf <= 1.0:
            conf = round(conf * 100)
        html = HTML.format(
            label=d.get("label", "-"),
            confidence=conf,
            category=d.get("category", "-"),
            temp=e.get("temperature", "-"),
            hum=e.get("humidity", "-"),
            status=e.get("status", "-"),
            ts=e.get("timestamp", "-"),
        )
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, *args):
        pass


print("[Dashboard] http://iotproject.local:8080")
HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
