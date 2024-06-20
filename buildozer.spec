[app]

# (str) Title of your application
title = SlingShotFX

# (str) Package name
package.name = slingshotfx

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = py,png,jpg,kv,atlas

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
requirements = kivy==2.0.0, kivymd==0.104.2, pillow, MetaTrader5

# (str) Supported orientations
orientation = portrait

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

android.add_aidl = src/main/aidl/foo/bar/IFoo.aidl

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY


#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (list) Android architecture to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup for Android
android.allow_backup = True


#
# iOS specific
#

# Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternatively, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# URL pointing to an icon (57x57px) to be displayed during download
# This option should be defined along with `app_url` and `full_size_image_url` options.
#ios.manifest.display_image_url =

# URL pointing to a large icon (512x512px) to be used by iTunes
# This option should be defined along with `app_url` and `display_image_url` options.
#ios.manifest.full_size_image_url =


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
