#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

python3 -m pip install --user -r requirements.txt

export PYTHONPATH="$HOME/.local/lib/python3.10/site-packages${PYTHONPATH:+:$PYTHONPATH}"

exec python3 -m streamlit run app.py --server.headless true --server.port 8501
