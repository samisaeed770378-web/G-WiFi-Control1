[app]
title = G-WiFi Control
package.name = gwificontrol
package.domain = com.sami

# Developer
# Engineer: Sami Al-Senawi
# Email: samisaeed770378@gmail.com

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,txt
version = 1.0.0

requirements = python3,kivy,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
