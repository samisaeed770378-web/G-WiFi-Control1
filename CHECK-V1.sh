#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$HOME/G-WiFi-Control"
python -m py_compile \
  main.py models.py router_manager.py network_tools.py security.py storage.py \
  router_models.py adapters/*.py
echo "========================================"
echo "G-WiFi Control V1 Python syntax: OK"
echo "========================================"
