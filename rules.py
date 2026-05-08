import threading
import time
from typing import Dict, List, Tuple, Any

# (user, ip) -> lista de timestamps (float) de eventos "login_failed"
FAILURES: Dict[Tuple[Any, Any], List[float]] = {}
_LOCK = threading.Lock()

WINDOW_SECONDS = 60


def _cleanup_old(ts_list: List[float], now: float) -> List[float]:
    cutoff = now - WINDOW_SECONDS
    return [t for t in ts_list if t >= cutoff]


def evaluate_log(parsed: dict) -> dict:
    """
    Evalúa un log normalizado y retorna un dict:
    { user, type, severity, message }
    """
    user = parsed.get("user", None)
    ip = parsed.get("ip", None)
    event = parsed.get("event", "")

    now = time.time()
    key = (user, ip)

    with _LOCK:
        if key not in FAILURES:
            FAILURES[key] = []

        # Limpieza para evitar crecimiento infinito
        FAILURES[key] = _cleanup_old(FAILURES[key], now)

        if event == "login_failed":
            FAILURES[key].append(now)
            FAILURES[key] = _cleanup_old(FAILURES[key], now)

            # Fuerza bruta: 5 o más fallos en ventana 60s
            if len(FAILURES[key]) >= 5:
                return {
                    "user": user,
                    "type": "BRUTE_FORCE",
                    "severity": "CRITICAL",
                    "message": f"Fuerza bruta detectada para user={user}, ip={ip}",
                }

            return {
                "user": user,
                "type": "NORMAL",
                "severity": "LOW",
                "message": "No issues detected",
            }

        if event == "login_success":
            # Login sospechoso: más de 3 fallos en ventana 60s antes del éxito
            failures_in_window = len(FAILURES[key])
            if failures_in_window > 3:
                return {
                    "user": user,
                    "type": "SUSPICIOUS_LOGIN",
                    "severity": "HIGH",
                    "message": (
                        f"Login exitoso sospechoso tras {failures_in_window} fallos recientes "
                        f"para user={user}, ip={ip}"
                    ),
                }

            return {
                "user": user,
                "type": "NORMAL",
                "severity": "LOW",
                "message": "No issues detected",
            }

        return {
            "user": user,
            "type": "NORMAL",
            "severity": "LOW",
            "message": "No issues detected",
        }
