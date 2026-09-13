from adapters.generic import GenericAdapter
from adapters.openwrt import OpenWrtAdapter
from adapters.mikrotik import MikroTikAdapter
from adapters.tplink import TPLinkAdapter
from adapters.huawei import HuaweiAdapter
from adapters.zte import ZTEAdapter


class RouterManager:
    ADAPTERS = {
        "Generic": GenericAdapter,
        "OpenWrt": OpenWrtAdapter,
        "MikroTik": MikroTikAdapter,
        "TP-Link": TPLinkAdapter,
        "Huawei": HuaweiAdapter,
        "ZTE": ZTEAdapter,
    }

    def __init__(self):
        self.adapter = None
        self.router_type = ""
        self.model = ""

    def connect(self, router_type, model, host, username, password):
        adapter_class = self.ADAPTERS.get(router_type)
        if not adapter_class:
            raise ValueError("Unsupported router type")

        adapter = adapter_class(host, username, password)

        if not adapter.test_connection():
            raise ConnectionError(
                "Unable to connect. Check URL, credentials, API availability, "
                "and that this is a router you are authorized to administer."
            )

        self.adapter = adapter
        self.router_type = router_type
        self.model = model
        return adapter.capabilities()

    def connected(self):
        return self.adapter is not None
