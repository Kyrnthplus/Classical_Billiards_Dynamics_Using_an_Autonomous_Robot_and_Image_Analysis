#!/bin/bash

# Script de limpeza para o Lemon Billiard
# Este script remove dados processados e resultados, mantendo apenas os dados brutos.

# Diretório raiz do script
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR" || exit 1

echo "Iniciando a limpeza do projeto..."

# 1. Limpa a pasta de dados processados (preservando o .gitkeep)
if [ -d "data/processed" ]; then
    echo "Limpando data/processed/..."
    find data/processed -type f ! -name ".gitkeep" -delete
fi

# 2. Limpa a pasta de resultados analíticos e gráficos (preservando o .gitkeep)
if [ -d "data/results" ]; then
    echo "Limpando data/results/..."
    find data/results -type f ! -name ".gitkeep" -delete
fi

# 3. Limpa arquivos de cache temporários do Python e arquivos de backup do editor
echo "Removendo caches e arquivos temporários..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*~" -delete 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

echo "Limpeza concluída com sucesso! (Dados brutos em data/raw/ preservados)"
