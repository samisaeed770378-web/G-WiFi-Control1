import requests
from urllib.parse import urljoin

class APIDiscovery:
    def __init__(self, host, username="", password=""):
        self.host = host.rstrip("/") + "/"
        self.session = requests.Session()
        self.session.auth = (username, password) if username else None
        self.session.headers.update({"User-Agent": "G-WiFi-Control/1.0"})

    def test(self, path):
        try:
            url = urljoin(self.host, path.lstrip("/"))
            r = self.session.get(url, timeout=4, allow_redirects=True)
            return {
                "path": path,
                "url": url,
                "status": r.status_code,
                "available": r.status_code < 500,
            }
        except requests.RequestException as e:
            return {
                "path": path,
                "url": urljoin(self.host, path.lstrip("/")),
                "status": 0,
                "available": False,
                "error": str(e),
            }

    def discover(self, vendor):
        vendor = vendor.lower().strip()

        candidates = {
            "openwrt": [
                "/ubus",
                "/cgi-bin/luci/",
            ],
            "mikrotik": [
                "/rest/system/resource",
                "/rest/",
            ],
            "tp-link": [
                "/",
                "/api/",
                "/api/v1/",
            ],
            "huawei": [
                "/",
                "/api/",
                "/api/v1/",
            ],
            "zte": [
                "/",
                "/api/",
                "/api/v1/",
            ],
        }

        paths = candidates.get(vendor, ["/", "/api/", "/api/v1/"])
        results = [self.test(p) for p in paths]

        for result in results:
            if result["available"] and result["status"] not in (404, 405):
                return {
                    "detected": True,
                    "endpoint": result["url"],
                    "status": result["status"],
                    "results": results,
                }

        return {
            "detected": False,
            "endpoint": "",
            "status": 0,
            "results": results,
        }
