#!/bin/bash

# Cleanup script for the Lemon Billiard project
# This script removes processed data and results, keeping only raw data files.

# Root directory of the script
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR" || exit 1

echo "Starting project cleanup..."

# 1. Cleans processed data folder (preserving .gitkeep)
if [ -d "data/processed" ]; then
    echo "Cleaning data/processed/..."
    find data/processed -type f ! -name ".gitkeep" -delete
fi

# 2. Cleans analytical results and plots folder (preserving .gitkeep)
if [ -d "data/results" ]; then
    echo "Cleaning data/results/..."
    find data/results -type f ! -name ".gitkeep" -delete
fi

# 3. Cleans Python temporary cache folders and editor backup files
echo "Removing caches and temporary files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*~" -delete 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

echo "Cleanup completed successfully! (Raw data in data/raw/ preserved)"
