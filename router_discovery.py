from router_models import vendors, models_for_vendor, firmwares_for, find_router
from api_discovery import APIDiscovery

def discover_router(vendor, model, firmware, host, username="", password=""):
    info = find_router(vendor, model, firmware)

    result = {
        "vendor": vendor,
        "model": model,
        "firmware": firmware,
        "host": host,
        "adapter": getattr(info, "adapter", "") if info else "",
        "api": getattr(info, "api", "") if info else "",
        "api_detected": False,
        "endpoint": "",
    }

    if not host:
        result["error"] = "Router URL is required"
        return result

    discovery = APIDiscovery(host, username, password)
    found = discovery.discover(vendor)

    result["api_detected"] = found["detected"]
    result["endpoint"] = found["endpoint"]
    result["http_status"] = found["status"]
    result["tests"] = found["results"]

    return result

if __name__ == "__main__":
    print("G-WiFi Control - Router Discovery")
    print("Available vendors:")
    for v in vendors():
        print(" -", v)
