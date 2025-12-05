#!/bin/bash

echo "🔧 (Re)Construindo a imagem..."
docker compose down
docker compose build

echo "🚀 Subindo a aplicação..."
docker compose up -d --build 

echo "✔ Aplicação disponível em: http://localhost:8080"
