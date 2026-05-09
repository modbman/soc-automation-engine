# SOC Automation Engine – Demo

Motor ligero de automatización para SOC (Security Operations Center) que recibe logs vía HTTP, normaliza eventos y detecta ataques de fuerza bruta utilizando ventanas temporales inteligentes.

---

# 🚀 Funcionalidades

- Ingesta de logs vía API REST (`POST /log`)
- Normalización flexible de eventos
- Detección de fuerza bruta:
  - 5 fallos desde misma IP + usuario en 60 segundos
  - Genera alerta `CRITICAL`
- Detección de login sospechoso:
  - Login exitoso después de múltiples fallos
  - Genera alerta `HIGH`
- Expiración automática de contadores
- Arquitectura modular
- Extensible a:
  - Slack
  - Discord
  - Telegram
  - Webhooks
  - SIEM externos
- Script automático de pruebas incluido

---

# 📦 Requisitos

- Python 3.12+
- pip

## Dependencias

- Flask
- Requests

---

# ⚙️ Instalación

## 1. Clonar proyecto

```bash
git clone https://github.com/tuusuario/soc-engine.git
cd soc-engine
```

## 2. Crear entorno virtual

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

# 📥 Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# ▶️ Ejecutar el servidor

```bash
python app.py
```

Servidor disponible en:

```text
http://localhost:5000
```

---

# 🧪 Pruebas manuales con curl

## Simular ataque de fuerza bruta

El quinto intento genera alerta `CRITICAL`.

```bash
for i in {1..5}; do
  curl -X POST http://localhost:5000/log \
    -H "Content-Type: application/json" \
    -d '{"user":"admin","ip":"192.168.1.100","event":"login_failed"}'
done
```

---

## Simular login sospechoso

Debe generar alerta `SUSPICIOUS_LOGIN`.

```bash
curl -X POST http://localhost:5000/log \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","ip":"192.168.1.100","event":"login_success"}'
```

---

# 🧪 Ejecutar pruebas automáticas

```bash
python test_demo.py
```

---

# 📁 Estructura del proyecto

```text
soc-engine/
│
├── app.py
├── ingest.py
├── parser.py
├── rules.py
├── alerting.py
├── test_demo.py
├── requirements.txt
├── iniciar.sh
└── README.md
```

---

# 🚨 Tipos de alertas

| Tipo | Severidad | Descripción |
|---|---|---|
| BRUTE_FORCE | CRITICAL | 5 fallos en menos de 60 segundos |
| SUSPICIOUS_LOGIN | HIGH | Login exitoso tras múltiples fallos |

---

# 🔒 Recomendaciones para producción

- Gunicorn
- Docker
- Redis
- PostgreSQL
- Integración SIEM
- MISP/TAXII

---

# ✒️ Autor

**modbman**

GitHub: https://github.com/modbman

---

# 📜 Licencia

MIT License
