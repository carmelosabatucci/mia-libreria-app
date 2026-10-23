[app]
title = Mia Libreria
package.name = applibreriaavanzata
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3==3.11.0,kivy
orientation = portrait
osx.kivy_version = 2.1.0
fullscreen = 0
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk_api = 24
android.private_storage = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
p4a.branch = release-2024.01.21
