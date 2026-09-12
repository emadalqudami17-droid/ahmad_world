[app]

# (str) Title of your application
title = Ahmed's World

# (str) Package name
package.name = ahmedworld

# (str) Package domain
package.domain = org.ahmedapp

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,wav,mp3

# (list) List of directories to exclude
source.exclude_dirs = tests,bin,venv,.buildozer,.git,__pycache__

# (str) Application versioning
version = 2.0

# (list) Application requirements
# IMPORTANT: Kivy 2.3.0 officially supports Python up to 3.12
requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.0,plyer
# (str) Icon of the application
icon.filename = %(source.dir)s/app_icon.png

# (str) Supported orientation
orientation = portrait

#
# Android specific
#

# (bool) Fullscreen
fullscreen = 1

# (list) Permissions
android.permissions = VIBRATE,INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept all SDK licenses
android.accept_sdk_license = True

# (str) Android architecture
android.archs = arm64-v8a

# (str) Presplash image
presplash.filename = %(source.dir)s/app_icon.png

# (bool) Enable AndroidX support
android.enable_androidx = True

#
# Python-for-Android
#

# Use the stable python-for-android branch
p4a.branch = master

# Use SDL2 bootstrap for Kivy
p4a.bootstrap = sdl2


[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
