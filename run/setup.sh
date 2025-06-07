#!/bin/bash
# This script sets up the development environment.
set -e

echo "--- Setting up Python virtual environment ---"
uv venv

echo "--- Installing Python dependencies ---"
uv pip install -r requirements.txt

echo "--- Installing Node.js dependencies ---"
npm install

echo "--- Build CSS ---"
npm run build

echo "--- Setup complete ---" 