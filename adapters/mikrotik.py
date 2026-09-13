import requests
from adapters.base import RouterAdapter
from models import RouterStatus, RouterCapabilities, WifiSettings, NetworkDevice


class MikroTikAdapter(RouterAdapter):
    def __init__(self, host, username, password):
        super().__init__(host, username, password)
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.api = self.host + "/rest"

    def request(self, method, path, **kwargs):
        r = self.session.request(
            method, self.api + path, timeout=8, **kwargs
        )
        r.raise_for_status()
        if r.text:
            return r.json()
        return {}

    def test_connection(self):
        try:
            self.request("GET", "/system/resource")
            return True
        except Exception:
            return False

    def capabilities(self):
        return RouterCapabilities(
            clients=True,
            block_client=False,
            wifi_settings=True,
            change_ssid=False,
            change_channel=False,
            reboot=True,
            wan_status=True,
            dhcp=True,
            firewall=True,
            traffic=True,
        )

    def get_status(self):
        try:
            data = self.request("GET", "/system/resource")
            if isinstance(data, list):
                data = data[0] if data else {}
            return RouterStatus(
                connected=True,
                hostname=data.get("board-name", "MikroTik"),
                firmware=data.get("version", ""),
                uptime=data.get("uptime", ""),
                wan_status="ONLINE",
            )
        except Exception as e:
            return RouterStatus(
                connected=False, hostname="MikroTik", wan_status=str(e)
            )

    def get_clients(self):
        clients = []
        try:
            data = self.request("GET", "/ip/arp")
            if isinstance(data, dict):
                data = [data]
            for item in data:
                mac = item.get("mac-address", "")
                ip = item.get("address", "")
                if mac:
                    clients.append(NetworkDevice(
                        name=mac, ip=ip, mac=mac, signal="-"
                    ))
        except Exception:
            pass
        return clients

    def block_client(self, mac):
        raise NotImplementedError(
            "V1 leaves firewall policy changes disabled until the router rules are explicitly mapped."
        )

    def unblock_client(self, mac):
        raise NotImplementedError(
            "V1 leaves firewall policy changes disabled until the router rules are explicitly mapped."
        )

    def get_wifi_settings(self):
        try:
            data = self.request("GET", "/interface/wifi")
            if isinstance(data, dict):
                data = [data]
            if not data:
                return WifiSettings()
            wifi = data[0]
            return WifiSettings(
                ssid=wifi.get("configuration.ssid", ""),
                channel=str(wifi.get("channel.frequency", "")),
            )
        except Exception as e:
            raise RuntimeError(f"Wi-Fi read failed: {e}")

    def update_wifi_settings(self, settings):
        raise NotImplementedError(
            "V1 does not write Wi-Fi settings; RouterOS Wi-Fi APIs vary by version/device."
        )

    def reboot(self):
        raise NotImplementedError(
            "V1 keeps reboot disabled until the exact RouterOS REST operation is verified."
        )
