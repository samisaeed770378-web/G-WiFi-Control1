from dataclasses import dataclass


@dataclass(frozen=True)
class RouterModel:
    vendor: str
    model: str
    firmware: str
    adapter: str
    api: str


ROUTERS = [
    RouterModel(
        "OpenWrt", "Generic OpenWrt", "22.x",
        "OpenWrtAdapter", "ubus JSON-RPC"
    ),
    RouterModel(
        "OpenWrt", "Generic OpenWrt", "23.x",
        "OpenWrtAdapter", "ubus JSON-RPC"
    ),
    RouterModel(
        "OpenWrt", "Generic OpenWrt", "24.x",
        "OpenWrtAdapter", "ubus JSON-RPC"
    ),

    RouterModel(
        "MikroTik", "Generic RouterOS", "6.x",
        "MikroTikAdapter", "RouterOS API"
    ),
    RouterModel(
        "MikroTik", "Generic RouterOS", "7.x",
        "MikroTikAdapter", "RouterOS REST"
    ),

    RouterModel(
        "TP-Link", "Archer", "Unknown",
        "TPLinkAdapter", "Model dependent"
    ),
    RouterModel(
        "TP-Link", "Home Router", "Unknown",
        "TPLinkAdapter", "Model dependent"
    ),

    RouterModel(
        "Huawei", "Home Router", "Unknown",
        "HuaweiAdapter", "Model dependent"
    ),

    RouterModel(
        "ZTE", "Home Router", "Unknown",
        "ZTEAdapter", "Model dependent"
    ),

    RouterModel(
        "Generic", "Generic Router", "Unknown",
        "GenericAdapter", "HTTP"
    ),
]


def vendors():
    """إرجاع الشركات المتاحة بدون تكرار."""
    return list(dict.fromkeys(r.vendor for r in ROUTERS))


def models_for_vendor(vendor):
    """إرجاع الموديلات الخاصة بالشركة."""
    return list(dict.fromkeys(
        r.model for r in ROUTERS
        if r.vendor.lower() == vendor.lower()
    ))


def firmwares_for(vendor, model):
    """إرجاع إصدارات Firmware المتاحة للموديل."""
    return list(dict.fromkeys(
        r.firmware for r in ROUTERS
        if r.vendor.lower() == vendor.lower()
        and r.model.lower() == model.lower()
    ))


def find_router(vendor, model, firmware):
    """العثور على تعريف الراوتر المناسب."""
    for router in ROUTERS:
        if (
            router.vendor.lower() == vendor.lower()
            and router.model.lower() == model.lower()
            and router.firmware.lower() == firmware.lower()
        ):
            return router

    return None


def adapters_for_vendor(vendor):
    """إرجاع الـAdapters الخاصة بالشركة."""
    return list(dict.fromkeys(
        r.adapter for r in ROUTERS
        if r.vendor.lower() == vendor.lower()
    ))


if __name__ == "__main__":
    print("G-WiFi Control Router Database")
    print("--------------------------------")

    for vendor in vendors():
        print(f"\n{vendor}")
        for model in models_for_vendor(vendor):
            print(f"  Model: {model}")
            for firmware in firmwares_for(vendor, model):
                router = find_router(vendor, model, firmware)
                print(
                    f"    Firmware: {firmware} | "
                    f"Adapter: {router.adapter} | "
                    f"API: {router.api}"
                )
