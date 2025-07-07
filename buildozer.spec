[app]
version = 1.0

# (str) Title of your application
title = SurveyApp

# (str) Package name
package.name = surveyapp

# (str) Package domain (used for Android package name)
package.domain = org.test

# (str) Source code where your main.py or SurveyApp1.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,csv

# (str) The main .py file to use as the main entry point
main.py = SurveyApp1.py

# (list) Application requirements (comma-separated)
requirements = python3,kivy

# (str) Supported orientation (one of: landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (bool) Hide the statusbar
android.hide_statusbar = 1

# (str) Android entry point, default is ok
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.theme = @android:style/Theme.NoTitleBar

# (bool) Use a custom source include (used when packaging .py files manually)
copy_to_apk = 1

# (bool) Presplash screen
android.presplash =

# (str) Presplash screen color (hex format, eg: #ffffff)
android.presplash_color = #ffffff

# (int) Target API (ensure it's installed in GitHub Actions)
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version
android.ndk = 23b

# (str) NDK API to use
android.ndk_api = 21

# (bool) Accept SDK license
android.accept_sdk_license = True

# (bool) Enable AndroidX
android.enable_androidx = True

# (str) Package format
android.packaging = zip

# (bool) Whether to copy library instead of linking (useful on GitHub Actions)
android.copy_libs = 1

# (str) Path to icon file
icon.filename = %(source.dir)s/icon.png

# (list) Permissions
android.permissions = INTERNET

# (str) Supported architectures
android.archs = arm64-v8a, armeabi-v7a


[buildozer]

# (str) Build target (only "android" is used here)
target = android
