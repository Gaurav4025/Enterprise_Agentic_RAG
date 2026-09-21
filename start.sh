#!/usr/bin/env bash
set -euo pipefail

export BACKEND_URL="${BACKEND_URL:-http://127.0.0.1:8000}"

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &

python -m streamlit run ui/app.py \
  --server.address 0.0.0.0 \
  --server.port "${PORT:-8501}" \
  --server.headless true \
  --browser.gatherUsageStats false
