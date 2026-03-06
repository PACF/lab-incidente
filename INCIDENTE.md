# Informe de Incidente
## 1. Resumen ejecutivo
Describir qué ocurrió, cómo se detectó y el impacto.
## 2. Alcance
- Entorno: GitHub Codespaces (contenedor Linux)
- Servicios: Web (Flask/Gunicorn) + SSH (openssh-server)
- Evidencia principal:
- logs/web_access.log
- logs/app.log
- logs/ssh_debug.log
- TIMELINE.csv
- ssh_timeline.csv
## 3. Cronología (Timeline)
Adjuntar TIMELINE.csv (web) y ssh_timeline.csv (ssh).
## 4. Hallazgos
- HTTP 404/500: rutas, timestamps, frecuencia
- Eventos SSH: failed/accepted, usuario, IP, puertos
- Correlación temporal: coincidencia entre scanning web y accesos SSH
## 5. Conclusiones
Patrones: scanning, fuerza bruta, credenciales débiles, etc.
## 6. Recomendaciones
- Deshabilitar login por contraseña
- Deshabilitar root
- llaves SSH
- rate limiting / fail2ban (si aplica)
- observabilidad y retención de logs