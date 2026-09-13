#!/data/data/com.termux/files/usr/bin/bash
set -u

cd "$HOME/G-WiFi-Control" || exit 1

echo "========================================"
echo " G-WiFi Control V2 CORE CHECK"
echo "========================================"

python -m py_compile \
main.py \
models.py \
router_manager.py \
router_models.py \
network_tools.py \
security.py \
storage.py \
api_discovery.py \
capabilities_engine.py \
router_discovery.py \
adapters/*.py

if [ $? -ne 0 ]; then
    echo
    echo "CORE CHECK: FAILED"
    exit 1
fi

echo
echo "CORE CHECK: OK"
echo

python - <<'PY'
from router_models import vendors, models_for_vendor, firmwares_for

print("VENDORS:")
for vendor in vendors():
    print("  •", vendor)

print()
print("ROUTER MODEL DATABASE: OK")
print("API DISCOVERY: READY")
print("CAPABILITIES ENGINE: READY")
PY

echo
echo "========================================"
echo " G-WiFi Control V2: READY"
echo "========================================"
