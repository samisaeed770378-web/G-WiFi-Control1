from dataclasses import dataclass


@dataclass
class NetworkDevice:
    name: str
    ip: str
    mac: str
    signal: str = "-"
    connected: bool = True
    blocked: bool = False


@dataclass
class WifiSettings:
    ssid: str = ""
    band: str = ""
    channel: str = ""
    security: str = ""


@dataclass
class RouterStatus:
    connected: bool = False
    hostname: str = ""
    firmware: str = ""
    uptime: str = ""
    wan_status: str = ""
    latency: float = 0.0


@dataclass
class RouterCapabilities:
    clients: bool = False
    block_client: bool = False
    wifi_settings: bool = False
    change_ssid: bool = False
    change_channel: bool = False
    reboot: bool = False
    wan_status: bool = False
    dhcp: bool = False
    firewall: bool = False
    wps: bool = False
    topology: bool = False
    traffic: bool = False

    def enabled(self):
        return {
            "clients": self.clients,
            "block_client": self.block_client,
            "wifi_settings": self.wifi_settings,
            "change_ssid": self.change_ssid,
            "change_channel": self.change_channel,
            "reboot": self.reboot,
            "wan_status": self.wan_status,
            "dhcp": self.dhcp,
            "firewall": self.firewall,
            "wps": self.wps,
            "topology": self.topology,
            "traffic": self.traffic,
        }
