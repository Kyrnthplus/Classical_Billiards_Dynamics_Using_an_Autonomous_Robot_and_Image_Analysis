#!/bin/bash

# Script de suporte para extração de quadros utilizando FFMPEG
# Uso: Executar a partir da raiz do projeto: ./data_pipeline/01_frame_extractor/extract_frames.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VIDEO_DIR="$ROOT_DIR/data/raw/video"

cd "$VIDEO_DIR" || exit 1

echo "Limpando diretório JPEG antigo..."
rm -rf JPEG
mkdir -p JPEG

# Loop sobre os arquivos de vídeo na pasta data/raw/video/
for i in *.mp4 *.MP4 *.avi *.AVI *.mkv *.mov; do
    # Verifica se o arquivo realmente existe
    [ -f "$i" ] || continue
    
    echo "Processando vídeo: $i"
    # Extrai os frames em escala de cinza, mantendo escala original e nomeando com base no vídeo
    ffmpeg -i "$i" -vf "scale=iw:ih,format=gray" "JPEG/${i%.*}-%07d.jpg"
done

if [ $? -eq 0 ]; then
    FRAME_COUNT=$(find JPEG -type f -name "*.jpg" 2>/dev/null | wc -l)
    echo "Sucesso! $FRAME_COUNT frames extraídos em 'data/raw/video/JPEG/'."
else
    echo "Erro ao processar os vídeos com ffmpeg."
    exit 1
fi
