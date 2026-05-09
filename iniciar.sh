
---

## 2. Crear el script `iniciar.sh`

```bash
cat > iniciar.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Entorno listo. Ejecutando servidor SOC Automation Engine..."
python app.py
EOF

chmod +x iniciar.sh