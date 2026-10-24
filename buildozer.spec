[app]
title = Mia Libreria
package.name = applibreriaavanzata
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# Requisiti allineati alla versione richiesta dal server
requirements = python3==3.14.2,kivy

orientation = portrait
osx.kivy_version = 2.1.0
fullscreen = 0

# Compilazione ultra-veloce solo per telefoni moderni a 64-bit
android.archs = arm64-v8a

android.api = 33
android.minapi = 24
android.ndk_api = 24
android.private_storage = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
