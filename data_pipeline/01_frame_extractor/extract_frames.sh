#!/bin/bash

# Slicing frame extraction support script using FFMPEG
# Usage: Run from the project root: ./data_pipeline/01_frame_extractor/extract_frames.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VIDEO_DIR="$ROOT_DIR/data/raw/video"

cd "$VIDEO_DIR" || exit 1

echo "Cleaning old JPEG directory..."
rm -rf JPEG
mkdir -p JPEG

# Loop over video files in data/raw/video/
for i in *.mp4 *.MP4 *.avi *.AVI *.mkv *.mov; do
    # Verify file exists
    [ -f "$i" ] || continue
    
    echo "Processing video: $i"
    # Extract frames in grayscale, keeping original scale and naming based on video
    ffmpeg -i "$i" -vf "scale=iw:ih,format=gray" "JPEG/${i%.*}-%07d.jpg"
done

if [ $? -eq 0 ]; then
    FRAME_COUNT=$(find JPEG -type f -name "*.jpg" 2>/dev/null | wc -l)
    echo "Success! $FRAME_COUNT frames extracted in 'data/raw/video/JPEG/'."
else
    echo "Error processing videos with ffmpeg."
    exit 1
fi
