#!/bin/bash

# Esperar a que el servicio esté listo
sleep 5

# Probar el endpoint de healthcheck
echo "Testing healthcheck endpoint..."
curl -v http://localhost:8000/health

# Probar el WebSocket endpoint
echo -e "\nTesting WebSocket endpoint..."
curl -v -N -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Host: localhost:8000" \
  -H "Origin: http://localhost:8000" \
  http://localhost:8000/ws 