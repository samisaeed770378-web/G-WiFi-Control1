import requests
from adapters.base import RouterAdapter
from models import RouterStatus, RouterCapabilities, WifiSettings


class GenericAdapter(RouterAdapter):
    def __init__(self, host, username, password):
        super().__init__(host, username, password)
        self.session = requests.Session()
        if username:
            self.session.auth = (username, password)

    def test_connection(self):
        try:
            r = self.session.get(self.host, timeout=5)
            return r.ok
        except Exception:
            return False

    def capabilities(self):
        return RouterCapabilities(
            clients=False,
            block_client=False,
            wifi_settings=False,
            change_ssid=False,
            change_channel=False,
            reboot=False,
            wan_status=False,
            dhcp=False,
            firewall=False,
            wps=False,
            topology=False,
            traffic=False,
        )

    def get_status(self):
        ok = self.test_connection()
        return RouterStatus(
            connected=ok,
            hostname="Generic Router",
            wan_status="ONLINE" if ok else "OFFLINE",
        )

    def get_clients(self):
        return []

    def block_client(self, mac):
        raise RuntimeError("Generic router has no verified client-control API.")

    def unblock_client(self, mac):
        raise RuntimeError("Generic router has no verified client-control API.")

    def get_wifi_settings(self):
        return WifiSettings()

    def update_wifi_settings(self, settings):
        raise RuntimeError("Generic router Wi-Fi API is not implemented.")

    def reboot(self):
        raise RuntimeError("Generic router reboot API is not implemented.")
