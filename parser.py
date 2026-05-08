from typing import Any, Dict


def parse_log(log: Dict[str, Any]) -> dict:
    """
    Normaliza el log de entrada a un formato estable.
    Asegura defaults con .get() para evitar errores ante claves faltantes.
    """
    return {
        "user": log.get("user", None),
        "ip": log.get("ip", None),
        "event": log.get("event", ""),
        "status": log.get("status", ""),
        "timestamp": log.get("timestamp", None),
    }
