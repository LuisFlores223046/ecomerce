"""gunicorn_config.py"""

import os

# Obtener el puerto de la variable de entorno, o usar 8001 como predeterminado
port = int(os.environ.get('PORT', 8001))

# Configuración para Gunicorn
bind = f"0.0.0.0:{port}"
workers = int(os.environ.get('WEB_CONCURRENCY', 4))
timeout = 120  # Segundos antes de que un worker se reinicie
worker_class = 'sync'  # Tipo de worker: sync, gevent, etc.

# Configuración de logging
loglevel = 'info'
accesslog = '-'  # Salida a stdout
errorlog = '-'   # Salida a stderr

# Captura de excepciones no manejadas
capture_output = True

# Comportamiento al recibir señales
graceful_timeout = 30  # Segundos para terminar trabajos pendientes