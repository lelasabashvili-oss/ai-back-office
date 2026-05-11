#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "❌ ANTHROPIC_API_KEY is not set."
  echo "   Run: export ANTHROPIC_API_KEY=your_key_here"
  exit 1
fi

echo "📦 Installing dependencies..."
pip3 install -r requirements.txt -q

echo "🚀 Starting ARIA — AI Back Office on http://localhost:8000"
python3 app.py
