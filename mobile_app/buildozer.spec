[app]

# App title
title = S-patch SDK Auto test

# Package name
package.name = sdkautotester

# Package domain
package.domain = com.wellysis

# App icon
android.icon.filename = %(source.dir)s/icon.png

# Custom Java source files (GattCallbackWrapper — extends abstract BluetoothGattCallback)
android.add_src = java

# Source directory
source.dir = .

# Source file patterns
source.include_exts = py,png,jpg,kv,atlas

# Version
version = 1.0.1

# Requirements (Android-compatible packages only)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,pillow

# Orientation (landscape, portrait, all)
orientation = portrait

# Fullscreen
fullscreen = 0

# Android permissions
# BLUETOOTH / BLUETOOTH_ADMIN : classic BLE pairing (all Android versions)
# BLUETOOTH_CONNECT / BLUETOOTH_SCAN : required on Android 12+ (API 31+)
# ACCESS_FINE_LOCATION : required for BLE scan on Android < 12
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,ACCESS_FINE_LOCATION

# Android API version
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# Architecture (arm64-v8a only to save build time)
android.archs = arm64-v8a

# Log level
log_level = 2

# Debug mode
debug = 1

[buildozer]

# Build directory
build_dir = ./.buildozer

# Bin directory
bin_dir = ./bin

# Log level
log_level = 2

# Warning on root
warn_on_root = 1
