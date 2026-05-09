cat > README.md << 'EOF'

\# SOC Automation Engine – Demo



Motor ligero de automatización para SOC (Security Operations Center) que recibe logs vía HTTP, normaliza eventos y detecta ataques de fuerza bruta con ventana temporal de 60 segundos.



\## 🚀 Funcionalidades



\- Ingesta de logs por API REST (POST `/log`)

\- Normalización flexible (soporta campos opcionales)

\- Detección de fuerza bruta: 5 fallos desde misma IP y usuario en 60 segundos → alerta `CRITICAL`

\- Login sospechoso tras fallos previos → alerta `HIGH`

\- Contadores independientes por `(usuario, IP)` con expiración automática

\- Alertas en consola (extensible a webhook, Slack, etc.)

\- Script de pruebas automáticas



\## 📦 Requisitos



\- Python 3.12+

\- Dependencias: `flask`, `requests`



\## ⚙️ Instalación y ejecución



```bash

\\# Clonar (o navegar a tu carpeta)

cd soc-engine



\\# Crear y activar entorno virtual

python -m venv venv

source venv/bin/activate   # En Windows: venv\\\\Scripts\\\\activate



\\# Instalar dependencias

pip install -r requirements.txt



\\# Ejecutar servidor

python app.py

🧪 Probar con curl

bash

\\# Enviar 5 fallos (el quinto activa la alerta)

for i in {1..5}; do

\&#x20; curl -X POST http://localhost:5000/log \\\\

\&#x20;   -H "Content-Type: application/json" \\\\

\&#x20;   -d '{"user":"admin","ip":"192.168.1.100","event":"login\\\_failed"}'

done



\\# Enviar login exitoso (debe dar SUSPICIOUS\\\_LOGIN)

curl -X POST http://localhost:5000/log \\\\

\&#x20; -H "Content-Type: application/json" \\\\

\&#x20; -d '{"user":"admin","ip":"192.168.1.100","event":"login\\\_success"}'

🧪 Prueba automática

bash

python test\\\_demo.py

📁 Estructura de archivos

app.py – punto de entrada



ingest.py – endpoint /log



parser.py – normaliza logs



rules.py – reglas de detección (ventana temporal)



alerting.py – muestra alertas en consola



test\\\_demo.py – batería de pruebas



requirements.txt – dependencias



iniciar.sh – script de inicio rápido



📌 Notas

Los contadores se limpian automáticamente después de 60 segundos sin actividad por cada (user, ip).



Para producción, reemplazar app.run por un servidor WSGI (gunicorn) y añadir cola de mensajes.



🛠️ Solución de problemas

Si pip install falla, asegúrate de haber activado el entorno virtual.



Si el puerto 5000 ya está ocupado, cambia el puerto en app.py (última línea).



Si no ves alertas, verifica que envías 5 fallos seguidos desde la misma IP y usuario antes de 60 segundos.



✒️ Autor

modbman – GitHub

EOF


