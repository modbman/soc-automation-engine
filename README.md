cat > README.md << 'EOF'
# SOC Automation Engine – Demo

Motor ligero de automatización para SOC (Security Operations Center) que recibe logs vía HTTP, normaliza eventos y detecta ataques de fuerza bruta con ventana temporal de 60 segundos.

## 🚀 Funcionalidades

- Ingesta de logs por API REST (POST `/log`)
- Normalización flexible (soporta campos opcionales)
- Detección de fuerza bruta: 5 fallos desde misma IP y usuario en 60 segundos → alerta `CRITICAL`
- Login sospechoso tras fallos previos → alerta `HIGH`
- Contadores independientes por `(usuario, IP)` con expiración automática
- Alertas en consola (extensible a webhook, Slack, etc.)
- Script de pruebas automáticas

## 📦 Requisitos

- Python 3.12+
- Dependencias: `flask`, `requests`

## ⚙️ Instalación y ejecución

```bash
# Clonar (o navegar a tu carpeta)
cd soc-engine

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py