FEATURE_NAMES = {
    "clients": "الأجهزة المتصلة",
    "block_client": "حظر جهاز",
    "wifi_settings": "إعدادات Wi-Fi",
    "change_ssid": "تغيير اسم الشبكة",
    "change_channel": "تغيير القناة",
    "reboot": "إعادة تشغيل الراوتر",
    "wan_status": "حالة الإنترنت WAN",
    "dhcp": "DHCP",
    "firewall": "الجدار الناري",
    "wps": "WPS",
    "topology": "خريطة الشبكة",
    "traffic": "مراقبة حركة المرور",
}

class CapabilitiesEngine:
    def __init__(self, adapter=None):
        self.adapter = adapter

    def detect(self):
        if not self.adapter:
            return {}

        try:
            caps = self.adapter.capabilities()
            if hasattr(caps, "__dict__"):
                data = caps.__dict__
            else:
                data = dict(caps)
        except Exception:
            return {}

        return {
            key: bool(value)
            for key, value in data.items()
            if key in FEATURE_NAMES
        }

    def supported_only(self):
        data = self.detect()
        return {
            key: FEATURE_NAMES[key]
            for key, enabled in data.items()
            if enabled and key in FEATURE_NAMES
        }

    @staticmethod
    def names(features):
        return [
            FEATURE_NAMES[key]
            for key in features
            if key in FEATURE_NAMES
        ]
