
import os
import time
import logging
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("txn-processor")

# Application configuration
APP_VERSION = os.getenv("APP_VERSION", "1.0")
DB_PASSWORD_FILE = os.getenv(
    "DB_PASSWORD_FILE",
    "/run/secrets/db_password"
)

def load_db_password():
    try:
        with open(DB_PASSWORD_FILE, "r") as secret:
            return secret.read().strip()
    except FileNotFoundError:
        return ""

DB_PASSWORD = load_db_password()

# Prometheus metrics
REQUEST_COUNT = Counter(
    "txn_requests_total",
    "Total payment authorization requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "txn_request_duration_seconds",
    "Payment API request latency",
    ["endpoint"],
    buckets=(0.05, 0.1, 0.2, 0.5, 1, 2, 3, 5)
)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION
    }), 200

@app.route("/authorize", methods=["POST"])
def authorize():
    start = time.time()
    status = "success"

    try:
        data = request.get_json(silent=True) or {}

        transaction_id = data.get("transaction_id")
        amount = data.get("amount")

        if not transaction_id or not isinstance(amount, (int, float)) or amount <= 0:
            status = "bad_request"
            return jsonify({"error": "Invalid payment request"}), 400

        # Simulate payment authorization processing
        time.sleep(0.1)

        logger.info("Payment authorization processed: %s", transaction_id)

        return jsonify({
            "transaction_id": transaction_id,
            "status": "approved",
            "version": APP_VERSION
        }), 200

    except Exception:
        status = "error"
        logger.exception("Payment authorization failed")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        duration = time.time() - start
        REQUEST_COUNT.labels("POST", "/authorize", status).inc()
        REQUEST_LATENCY.labels("/authorize").observe(duration)

@app.route("/metrics", methods=["GET"])
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }
@app.route("/config-check", methods=["GET"])
def config_check():
    return jsonify({
        "secret_loaded": bool(DB_PASSWORD),
        "secret_exposed": False
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
