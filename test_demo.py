import json
import time

import requests

URL = "http://localhost:5000/log"


def pretty(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)


def post_log(log):
    print("\n=== ENVÍO ===")
    print(pretty(log))
    try:
        resp = requests.post(URL, json=log, timeout=10)
        print("\n=== RESPUESTA HTTP ===")
        print("Status code:", resp.status_code)
        try:
            print(pretty(resp.json()))
        except Exception:
            print(resp.text)
        return resp
    except requests.exceptions.ConnectionError:
        print("\n❌ No se pudo conectar al servidor.")
        print("Ejecuta primero: python app.py (mantén el servidor corriendo).")
        return None


def main():
    user = "admin"
    ip1 = "192.168.1.100"

    # a) Enviar 3 fallos: expect severity LOW (sin alerta crítica)
    print("\n*** Caso a) 3 fallos: expect severity LOW (sin CRITICAL) ***")
    post_log({"user": user, "ip": ip1, "event": "login_failed"})
    post_log({"user": user, "ip": ip1, "event": "login_failed"})
    post_log({"user": user, "ip": ip1, "event": "login_failed"})

    # b) +2 fallos más desde misma IP/usuario => llegar a 5 => CRITICAL / BRUTE_FORCE
    print("\n*** Caso b) +2 fallos (llegar a 5): expect CRITICAL / BRUTE_FORCE ***")
    post_log({"user": user, "ip": ip1, "event": "login_failed"})
    post_log({"user": user, "ip": ip1, "event": "login_failed"})

    # c) login_success después de los fallos => HIGH / SUSPICIOUS_LOGIN
    print("\n*** Caso c) login_success tras fallos: expect HIGH / SUSPICIOUS_LOGIN ***")
    post_log({"user": user, "ip": ip1, "event": "login_success"})

    # d) 5 fallos desde IP diferente => también BRUTE_FORCE
    ip2 = "10.0.0.99"
    print("\n*** Caso d) 5 fallos en IP distinta: expect CRITICAL / BRUTE_FORCE ***")
    for _ in range(5):
        post_log({"user": user, "ip": ip2, "event": "login_failed"})

    # e) Esperar 61s => expira ventana de 60s; nuevo fallo no debe dar CRITICAL
    print("\n*** Caso e) sleep 61s para expirar ventana: expect que NO vuelva CRITICAL ***")
    time.sleep(61)
    post_log({"user": user, "ip": ip1, "event": "login_failed"})


if __name__ == "__main__":
    main()
