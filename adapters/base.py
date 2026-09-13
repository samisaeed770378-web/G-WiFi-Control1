from abc import ABC, abstractmethod
from models import RouterStatus, RouterCapabilities, WifiSettings


class RouterAdapter(ABC):
    def __init__(self, host, username, password):
        self.host = host.rstrip("/")
        self.username = username
        self.password = password

    @abstractmethod
    def test_connection(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def capabilities(self) -> RouterCapabilities:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> RouterStatus:
        raise NotImplementedError

    @abstractmethod
    def get_clients(self):
        raise NotImplementedError

    @abstractmethod
    def block_client(self, mac):
        raise NotImplementedError

    @abstractmethod
    def unblock_client(self, mac):
        raise NotImplementedError

    @abstractmethod
    def get_wifi_settings(self):
        raise NotImplementedError

    @abstractmethod
    def update_wifi_settings(self, settings: WifiSettings):
        raise NotImplementedError

    @abstractmethod
    def reboot(self):
        raise NotImplementedError
