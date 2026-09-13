import socket
import time
import requests


def ping_test(host="8.8.8.8", port=53, timeout=2):
    start = time.perf_counter()
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        elapsed = (time.perf_counter() - start) * 1000
        return {"success": True, "latency": round(elapsed, 2)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def dns_test():
    try:
        start = time.perf_counter()
        ip = socket.gethostbyname("google.com")
        elapsed = (time.perf_counter() - start) * 1000
        return {"success": True, "ip": ip, "latency": round(elapsed, 2)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def internet_test():
    try:
        start = time.perf_counter()
        r = requests.get(
            "https://connectivitycheck.gstatic.com/generate_204",
            timeout=5
        )
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "success": r.status_code in (200, 204),
            "latency": round(elapsed, 2)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def network_diagnosis():
    ping = ping_test()
    dns = dns_test()
    internet = internet_test()
    problems = []

    if not ping["success"]:
        problems.append("Ping test failed")
    if not dns["success"]:
        problems.append("DNS resolution failed")
    if not internet["success"]:
        problems.append("Internet connectivity failed")

    return {
        "status": "HEALTHY" if not problems else "PROBLEM",
        "ping": ping,
        "dns": dns,
        "internet": internet,
        "problems": problems,
    }
