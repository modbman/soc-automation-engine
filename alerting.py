import json
from typing import Optional

import requests

WEBHOOK_URL: Optional[str] = None


def send_alert(alert: dict) -> None:
    """
    Envía/propaga una alerta.
    Para demo: imprime con formato claro en consola.
    Si WEBHOOK_URL no es None: realiza POST y atrapa excepciones.
    """
    try:
        print(f"🚨 ALERT: {json.dumps(alert, ensure_ascii=False)}")
    except Exception:
        print("🚨 ALERT:", alert)

    if WEBHOOK_URL is None:
        return

    try:
        requests.post(WEBHOOK_URL, json=alert, timeout=5)
    except Exception as e:
        print(f"⚠️ Webhook falló: {e}")
