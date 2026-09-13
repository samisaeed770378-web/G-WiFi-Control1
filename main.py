import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen

from router_manager import RouterManager
from router_models import ROUTER_MODELS
from network_tools import ping_test, dns_test, internet_test, network_diagnosis
from storage import save_router, load_router

router_manager = RouterManager()


class Dashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        root.add_widget(Label(
            text="[b]G-WiFi Control V1[/b]",
            markup=True, font_size=dp(26),
            size_hint_y=None, height=dp(55)
        ))

        self.status = Label(
            text="● Router: Not Connected",
            size_hint_y=None, height=dp(45)
        )
        root.add_widget(self.status)

        stats = GridLayout(cols=3, size_hint_y=None, height=dp(80))
        self.devices = Label(text="Devices\n0")
        self.latency = Label(text="Latency\n-")
        self.signal = Label(text="Signal\n-")
        stats.add_widget(self.devices)
        stats.add_widget(self.latency)
        stats.add_widget(self.signal)
        root.add_widget(stats)

        buttons = GridLayout(cols=2, spacing=dp(8))
        for text, screen in [
            ("📱 Devices", "devices"),
            ("📶 Wi-Fi", "wifi"),
            ("🔐 Security", "security"),
            ("🛠 Tools", "tools"),
            ("⚙ Router", "router"),
            ("🧠 Diagnosis", "diagnosis"),
        ]:
            b = Button(text=text)
            b.bind(on_press=lambda x, s=screen: setattr(self.manager, "current", s))
            buttons.add_widget(b)
        root.add_widget(buttons)
        self.add_widget(root)

    def refresh(self):
        if not router_manager.connected():
            self.status.text = "● Router: Not Connected"
            self.devices.text = "Devices\n0"
            return
        try:
            status = router_manager.adapter.get_status()
            self.status.text = (
                f"● {router_manager.router_type} / "
                f"{router_manager.model} • {status.wan_status}"
            )
            try:
                self.devices.text = (
                    f"Devices\n{len(router_manager.adapter.get_clients())}"
                )
            except Exception:
                self.devices.text = "Devices\n-"
        except Exception as e:
            self.status.text = f"Error: {e}"


class RouterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(7))

        root.add_widget(Label(
            text="[b]Router Connection[/b]", markup=True, font_size=dp(24),
            size_hint_y=None, height=dp(45)
        ))

        self.router_type = Spinner(
            text="Generic", values=tuple(ROUTER_MODELS.keys()),
            size_hint_y=None, height=dp(50)
        )
        self.router_type.bind(text=self.brand_changed)
        root.add_widget(self.router_type)

        self.router_model = Spinner(
            text="Generic Router",
            values=tuple(ROUTER_MODELS["Generic"]),
            size_hint_y=None, height=dp(50)
        )
        root.add_widget(self.router_model)

        self.firmware = TextInput(
            hint_text="Firmware / OS version (optional)",
            multiline=False, size_hint_y=None, height=dp(50)
        )
        root.add_widget(self.firmware)

        self.host = TextInput(
            text="http://192.168.1.1",
            hint_text="Router URL / IP",
            multiline=False, size_hint_y=None, height=dp(50)
        )
        root.add_widget(self.host)

        self.username = TextInput(
            hint_text="Username",
            multiline=False, size_hint_y=None, height=dp(50)
        )
        root.add_widget(self.username)

        self.password = TextInput(
            hint_text="Password",
            password=True, multiline=False, size_hint_y=None, height=dp(50)
        )
        root.add_widget(self.password)

        connect = Button(
            text="CONNECT & DETECT CAPABILITIES",
            size_hint_y=None, height=dp(58)
        )
        connect.bind(on_press=lambda x: self.connect())
        root.add_widget(connect)

        self.result = Label(text="Ready", halign="left", valign="top")
        root.add_widget(self.result)

        back = Button(text="← Dashboard", size_hint_y=None, height=dp(48))
        back.bind(on_press=lambda x: setattr(self.manager, "current", "dashboard"))
        root.add_widget(back)

        self.add_widget(root)

    def brand_changed(self, spinner, brand):
        models = ROUTER_MODELS.get(brand, ["Generic Router"])
        self.router_model.values = tuple(models)
        self.router_model.text = models[0]

    def connect(self):
        self.result.text = "Connecting..."
        brand = self.router_type.text
        model = self.router_model.text
        host = self.host.text.strip()
        username = self.username.text
        password = self.password.text
        firmware = self.firmware.text.strip()

        def worker():
            try:
                caps = router_manager.connect(
                    brand, model, host, username, password
                )
                enabled = [
                    k for k, v in caps.enabled().items() if v
                ]
                message = (
                    f"CONNECTED ✓\n\n"
                    f"Brand: {brand}\n"
                    f"Model: {model}\n"
                    f"Firmware: {firmware or 'Router API'}\n\n"
                    f"SUPPORTED:\n"
                    + ("\n".join(enabled) if enabled else "None")
                )
                save_router({
                    "brand": brand,
                    "model": model,
                    "firmware": firmware,
                    "host": host,
                    "username": username,
                })
            except Exception as e:
                message = f"CONNECTION FAILED\n\n{e}"

            Clock.schedule_once(lambda dt: setattr(self.result, "text", message))
            Clock.schedule_once(
                lambda dt: self.manager.get_screen("dashboard").refresh()
            )

        threading.Thread(target=worker, daemon=True).start()


class ToolsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        root.add_widget(Label(
            text="[b]Network Tools[/b]", markup=True, font_size=dp(24),
            size_hint_y=None, height=dp(50)
        ))
        self.output = Label(text="Ready")
        root.add_widget(self.output)

        for title, fn in [
            ("Ping Test", ping_test),
            ("DNS Test", dns_test),
            ("Internet Test", internet_test),
            ("Full Diagnosis", network_diagnosis),
        ]:
            b = Button(text=title, size_hint_y=None, height=dp(52))
            b.bind(on_press=lambda x, f=fn: self.execute(f))
            root.add_widget(b)

        back = Button(text="← Dashboard", size_hint_y=None, height=dp(48))
        back.bind(on_press=lambda x: setattr(self.manager, "current", "dashboard"))
        root.add_widget(back)
        self.add_widget(root)

    def execute(self, function):
        self.output.text = "Running..."

        def worker():
            try:
                result = function()
                text = str(result)
            except Exception as e:
                text = str(e)
            Clock.schedule_once(lambda dt: setattr(self.output, "text", text))

        threading.Thread(target=worker, daemon=True).start()


class DevicesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        root.add_widget(Label(
            text="[b]Connected Devices[/b]", markup=True, font_size=dp(24),
            size_hint_y=None, height=dp(50)
        ))
        self.list_box = BoxLayout(
            orientation="vertical", spacing=dp(7), size_hint_y=None
        )
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.list_box)
        root.add_widget(scroll)

        refresh = Button(text="Refresh Devices", size_hint_y=None, height=dp(50))
        refresh.bind(on_press=lambda x: self.refresh())
        root.add_widget(refresh)

        back = Button(text="← Dashboard", size_hint_y=None, height=dp(48))
        back.bind(on_press=lambda x: setattr(self.manager, "current", "dashboard"))
        root.add_widget(back)
        self.add_widget(root)

    def refresh(self):
        self.list_box.clear_widgets()
        if not router_manager.connected():
            self.list_box.add_widget(Label(text="Connect a router first"))
            return
        try:
            devices = router_manager.adapter.get_clients()
            if not devices:
                self.list_box.add_widget(
                    Label(text="No devices returned by the selected router API.")
                )
                return
            for device in devices:
                row = BoxLayout(size_hint_y=None, height=dp(75))
                row.add_widget(Label(
                    text=f"{device.name}\n{device.ip} • {device.mac}\n{device.signal}"
                ))
                self.list_box.add_widget(row)
        except Exception as e:
            self.list_box.add_widget(Label(text=str(e)))


class WifiScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        root.add_widget(Label(
            text="[b]Wi-Fi[/b]", markup=True, font_size=dp(24),
            size_hint_y=None, height=dp(50)
        ))
        self.info = Label(text="Connect a supported router.")
        root.add_widget(self.info)

        b = Button(text="READ WI-FI SETTINGS", size_hint_y=None, height=dp(55))
        b.bind(on_press=lambda x: self.refresh())
        root.add_widget(b)

        back = Button(text="← Dashboard", size_hint_y=None, height=dp(48))
        back.bind(on_press=lambda x: setattr(self.manager, "current", "dashboard"))
        root.add_widget(back)
        self.add_widget(root)

    def refresh(self):
        if not router_manager.connected():
            self.info.text = "Router not connected."
            return
        try:
            s = router_manager.adapter.get_wifi_settings()
            self.info.text = (
                f"SSID: {s.ssid or '-'}\n"
                f"Band: {s.band or '-'}\n"
                f"Channel: {s.channel or '-'}\n"
                f"Security: {s.security or '-'}"
            )
        except Exception as e:
            self.info.text = str(e)


class SecurityScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(10))
        root.add_widget(Label(
            text="[b]Security Center[/b]", markup=True, font_size=dp(24),
            size_hint_y=None, height=dp(50)
        ))
        root.add_widget(Label(
            text=(
                "V1 shows only verified information from the router API.\n\n"
                "Encryption / Firewall / WPS / Threat status are not fabricated.\n"
                "They will become active when the selected adapter exposes them."
            )
        ))
        back = Button(text="← Dashboard", size_hint_y=None, height=dp(48))
        back.bind(on_press=lambda x: setattr(self.manager, "current", "dashboard"))
        root.add_widget(back)
        self.add_widget(root)


class DiagnosisScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(10))
        root.add_widget(Label(
            text="[b]Network Diagnosis[/b]", markup=True, font_size=dp(24),
            size_hint_y=None, height=dp(50)
        ))
        self.output = Label(text="Ready")
        root.add_widget(self.output)
        b = Button(text="RUN DIAGNOSIS", size_hint_y=None, height=dp(60))
        b.bind(on_press=lambda x: self.run())
        root.add_widget(b)
        back = Button(text="← Dashboard", size_hint_y=None, height=dp(48))
        back.bind(on_press=lambda x: setattr(self.manager, "current", "dashboard"))
        root.add_widget(back)
        self.add_widget(root)

    def run(self):
        self.output.text = "Running..."
        def worker():
            result = network_diagnosis()
            text = (
                f"STATUS: {result['status']}\n\n"
                f"PING: {result['ping']}\n\n"
                f"DNS: {result['dns']}\n\n"
                f"INTERNET: {result['internet']}\n\n"
                f"PROBLEMS: {result['problems']}"
            )
            Clock.schedule_once(lambda dt: setattr(self.output, "text", text))
        threading.Thread(target=worker, daemon=True).start()


class GWiFiApp(App):
    def build(self):
        manager = ScreenManager()
        for screen, name in [
            (Dashboard(), "dashboard"),
            (DevicesScreen(), "devices"),
            (WifiScreen(), "wifi"),
            (SecurityScreen(), "security"),
            (ToolsScreen(), "tools"),
            (RouterScreen(), "router"),
            (DiagnosisScreen(), "diagnosis"),
        ]:
            manager.add_widget(screen)
        return manager


if __name__ == "__main__":
    GWiFiApp().run()
