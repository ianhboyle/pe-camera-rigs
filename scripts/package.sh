#!/bin/bash
# Package PE Camera Rigs addon for distribution
# Usage: ./package.sh [version]
# Example: ./package.sh 1.1.0

set -e  # Exit on error

# Get version from argument or default to 'dev'
VERSION=${1:-dev}

# Get project root directory (one level up from scripts/)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📦 Packaging PE Camera Rigs v${VERSION}..."

# Create dist directory if it doesn't exist
mkdir -p dist

# Package the addon
OUTPUT_FILE="$PROJECT_ROOT/dist/pe_camera_rigs_v${VERSION}.zip"

# Remove old zip if it exists
rm -f "$OUTPUT_FILE"

# Create new zip from src directory
cd "$PROJECT_ROOT/src"
zip -r "$OUTPUT_FILE" pe_camera_rigs \
  -x "*/\.*" \
  -x "*/__pycache__/*" \
  -x "*.pyc" \
  -x "*.pyo" \
  -x "*~"

cd "$PROJECT_ROOT"

# Verify the zip
echo ""
echo "✅ Package created: dist/pe_camera_rigs_v${VERSION}.zip"
echo ""
echo "📋 Contents preview:"
unzip -l "$OUTPUT_FILE" | head -20

# Show file size
SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
echo ""
echo "📊 Package size: $SIZE"

echo ""
echo "✨ Done! Upload this file to GitHub Releases."
