import requests
from adapters.base import RouterAdapter
from models import RouterStatus, RouterCapabilities, WifiSettings, NetworkDevice


class OpenWrtAdapter(RouterAdapter):
    def __init__(self, host, username, password):
        super().__init__(host, username, password)
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.rpc = self.host + "/ubus"

    def rpc_call(self, object_name, method, params):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "call",
            "params": ["0" * 32, object_name, method, params],
        }
        r = self.session.post(self.rpc, json=payload, timeout=8)
        r.raise_for_status()
        data = r.json()
        if data.get("error"):
            raise RuntimeError(str(data["error"]))
        return data

    def test_connection(self):
        try:
            self.rpc_call("system", "board", {})
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
            topology=False,
            traffic=False,
        )

    def get_status(self):
        try:
            result = self.rpc_call("system", "board", {})
            data = result.get("result", [])
            info = data[1] if len(data) > 1 else {}
            release = info.get("release", {})
            return RouterStatus(
                connected=True,
                hostname=info.get("hostname", "OpenWrt"),
                firmware=release.get("description", ""),
                wan_status="ONLINE",
            )
        except Exception as e:
            return RouterStatus(
                connected=False, hostname="OpenWrt", wan_status=str(e)
            )

    def get_clients(self):
        clients = []
        for interface in ("hostapd.wlan0", "hostapd.wlan1"):
            try:
                result = self.rpc_call(interface, "get_clients", {})
                data = result.get("result", [])
                stations = data[1] if len(data) > 1 else {}
                for mac, info in stations.items():
                    signal = info.get("signal", "-")
                    clients.append(NetworkDevice(
                        name=mac, ip="Unknown", mac=mac,
                        signal=f"{signal} dBm"
                    ))
            except Exception:
                continue
        return clients

    def block_client(self, mac):
        raise NotImplementedError(
            "MAC blocking requires detecting the actual OpenWrt firewall setup first."
        )

    def unblock_client(self, mac):
        raise NotImplementedError(
            "MAC unblocking requires detecting the actual OpenWrt firewall setup first."
        )

    def get_wifi_settings(self):
        self.rpc_call("uci", "get", {"config": "wireless"})
        return WifiSettings()

    def update_wifi_settings(self, settings):
        raise NotImplementedError(
            "SSID/channel update requires mapping the detected wireless section."
        )

    def reboot(self):
        self.rpc_call("system", "reboot", {})
        return True
