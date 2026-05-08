from flask import Flask, request, jsonify

from parser import parse_log
from rules import evaluate_log
from alerting import send_alert

app = Flask(__name__)


@app.route("/log", methods=["POST"])
def ingest_log():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return (
            jsonify(
                {
                    "status": "error",
                    "result": {
                        "severity": "LOW",
                        "type": "INVALID_PAYLOAD",
                        "message": "Body JSON inválido o no es un objeto",
                    },
                }
            ),
            400,
        )

    parsed = parse_log(payload)
    result = evaluate_log(parsed)

    severity = (result or {}).get("severity")
    if severity in {"HIGH", "CRITICAL"}:
        send_alert({"parsed": parsed, "alert": result})

    return jsonify({"status": "processed", "result": result}), 200
