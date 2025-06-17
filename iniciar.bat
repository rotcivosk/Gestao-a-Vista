@echo off
start dist\run.exe
timeout /t 2
start http://127.0.0.1:8000/frontend/index.html
echo "Aplicação iniciando..."
