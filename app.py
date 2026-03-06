import os
import time
import uuid
from datetime import datetime, timezone
from flask import Flask,request, jsonify

app = Flask(__name__)

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
WEB_LOG = os.path.join(LOG_DIR, "web_access.log")
APP_LOG = os.path.join(LOG_DIR, "app.log")

def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def write_line(path: str, line: str):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

@app.before_request
def start_timer_and_request_id():
    request._start_time = time.time()
    request._id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

@app.after_request
def log_request(response):
    duration_ms = int((time.time() - getattr(request, "_start_time", time.time())) * 1000)
    rid = getattr(request, "_rid", "-")
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "-"
    line = (
        f'{utc_now_iso()} rid={rid} ip={client_ip} '
        f'method={request.method} path="{request.path}" '
        f'status={response.status_code} dur_ms={duration_ms} ua="{request.headers.get("User-Agent","-")}"'
        )
    write_line(WEB_LOG, line)
    return response

@app.route("/")
def index():
    return """
    <h1>Lab Incidente - Codespaces</h1>
    <ul>
    <li><a href="/ok">/ok</a> (200)</li>
    <li><a href="/no-existe">/no-existe</a> (404)</li>
    <li><a href="/boom">/boom</a> (500)</li>
    <li><a href="/health">/health</a> (200 JSON)</li>
    </ul>
    """

@app.route("/ok")
def ok():
    return "OK 200\n", 200

@app.route("/boom")
def boom():
    raise RuntimeError("Error forzado para laboratorio (500).")

@app.route("/health")
def health():
    return jsonify(status="up", time_utc=utc_now_iso()), 200

@app.errorhandler(404)
def not_found(e):
    write_line(APP_LOG, f"{utc_now_iso()} level=warn event=404, path={request.path}")
    return "404 Not Found\n", 404

@app.errorhandler(500)
def internal_error(e):
    write_line(APP_LOG, f"{utc_now_iso()} level=error event=500, path={request.path} err={repr(e)}")
    return "500 Internal Server Error\n", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)