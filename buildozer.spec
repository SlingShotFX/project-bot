[app]

# Title of your application
title = SlingShotFX

# Package name
package.name = slingshotfx

# Package domain (needed for android/ios packaging)
package.domain = org.example

# Source code where the main.py lives
source.dir = py,png,jpg,kv,atlas

# Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# Application version
version = 0.1

# Application requirements
requirements = kivy==2.0.0, kivymd==0.104.2, pillow, MetaTrader5

# Supported orientations
orientation = portrait

# Specify AIDL files to include
android.add_aidl = src/main/aidl/foo/bar/IFoo.aidl

# Specify output directory for generated Java source files (if needed)
# android.add_src = path/to/generated/java/source

# Specify header directory for C++ headers (if needed)
# android.add_cpp = path/to/generated/cpp/headers

# Indicate if the application should be fullscreen or not
fullscreen = 0

# Permissions
android.permissions = INTERNET

# Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# Allow backup for Android
android.allow_backup = True

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
