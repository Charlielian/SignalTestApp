[app]

# (str) Title of your application
title = SignalTestApp

# (str) Package name
package.name = signal_test_app

# (str) Package domain (needed for android/ios packaging)
package.domain = com.signal

# (str) Source code where the main.py live
source.dir = src

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs =

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.png

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pillow,pandas,openpyxl,requests,cython

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#
# (str) Path to a custom kivy_ios directory
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
#ios.kivy_ios_branch = master

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities with provisioning_tool.py -v
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names: 
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray, 
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy, 
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples and https://airbnb.design/lottie/ 
# for general documentation. 
# Lottie files can be created using various tools, like Adobe After Effect or Synfig.
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
#android.adaptive_icon_background = "#FFFFFF"
#android.adaptive_icon_foreground = "%(source.dir)s/data/icon_fg.png"

# (list) Permissions
# (See https://python-for-android.readthedocs.io/en/latest/buildoptions/#build-options-1 for all the supported syntaxes and properties)
android.permissions = CAMERA, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE, MODIFY_PHONE_STATE

# (list) features (adds uses-feature -tags to manifest)
#android.features = android.hardware.camera

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 23

# (int) Android SDK version to use
android.sdk = 31

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 23

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_dir = 

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_dir = 

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_dir = 

# (bool) If True, then skip trying to update the Android sdk 
# This can be useful to avoid excess Internet downloads or save time 
# when an update is due and you just want to test/build your package 
# android.skip_update = False

# (bool) If True, then automatically accept SDK license 
# agreements. This is intended for automation only. If set to False, 
# the default, you will be shown the license when first running 
# buildozer. 
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# use that parameter together with android.entrypoint to set custom Java class instead of PythonActivity
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# use that parameter to add permissions or other tags not covered by android.permissions
#android.extra_manifest_xml = <uses-permission android:name="android.permission.READ_PHONE_STATE" />

# (str) Extra xml to write directly inside the <application> element of AndroidManifest.xml
# use that parameter to add activities, services or other components.
#android.extra_application_xml = 

# (str) Full name including package path of the Java class that implements Python Service
# use that parameter to set custom Java class instead of PythonService
#android.service_class_name = org.kivy.android.PythonService

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = @android:style/Theme.Holo.Light

# (list) Pattern to whitelist for the whole project
#android.whitelist = 

# (str) Path to a custom whitelist file
#android.whitelist_src = 

# (str) Path to a custom blacklist file
#android.blacklist_src = 

# (list) List of Java .jar files to add to the libs so that pyjnius can access it
#android.add_jars = foo.jar,bar.jar,path/to/more/jars

# (list) List of Java files to add to the android project (can be java or a directory containing the files)
#android.add_src = 

# (list) Android AAR archives to add
#android.add_aars = 

# (list) Gradle dependencies to add
#android.gradle_dependencies = 

# (list) add java compile options
# this can for example be necessary if you're using the androidx libraries
# see https://developer.android.com/studio/write/java8-support for further information
# android.add_compile_options = "--source 1.8", "--target 1.8"

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes
# android.gradle_repositories = "maven { url 'https://kotlin.bintray.com/ktor' }", "maven { url 'https://jitpack.io' }"

# (list) packaging options to add
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle dependencies
# android.add_packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'"

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters = 

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (str) screenOrientation to set for the main activity.
# Valid values can be found at https://developer.android.com/guide/topics/manifest/activity-element.html#screen
#android.manifest.orientation = fullSensor

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data = 

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
#android.uses_library =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (list) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = armeabi-v7a,arm64-v8a

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be edited if you know what you're doing
# android.numeric_version = 1

# (bool) enables Android's bundle format (AAB)
# android.use_aab = False

# (str) path to build artifact(s) to return (in case of multiple artifacts, pick the one to return)
# android.buildartifact = "dist/{app.name}-{version}.apk"

# (str) the name of the directory where buildozer should look for your own build.gradle
# this is useful if you need to override the default build.gradle
# android.build.gradle_dir = custom_buildgradle

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
#p4a.source_dir = ../python-for-android

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.git_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes = 

# (str) Filename to the hook for p4a
#p4a.hook = 

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port = 

# Control passing the --use-setup-py vs --ignore-setup-py to p4a
# "infer" will set --use-setup-py if there's a setup.py in the source directory
#p4a.setup_py = infer

# (str) extra command line arguments to pass to p4a
#p4a.extra_args = 

# (bool) Create a blacklist.txt file with that contains the non-public modules
#p4a.blacklist = False

# (bool) Use --debug mode for p4a
#p4a.debug_build = False

# (str) The built application icon: 
#p4a.icon = %(source.dir)s/data/icon.png

# (str) The built application presplash: 
#p4a.presplash = %(source.dir)s/data/presplash.png

# (str) The color of the status bar at the top of the screen
#p4a.statusbar_color = 

# (bool) Enable androidX support. Enable when you use androidX dependencies or want to
# use newer android libraries.
#p4a.androidx = True


#
# iOS specific
#

# (str) Path to a custom kivy-ios directory
#ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities with provisioning_tool.py -v
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

# (str) Provisioning profile to use for the debug version
#ios.provisioning_profile.debug = "path/to/profile"

# (str) Provisioning profile to use for the release version
#ios.provisioning_profile.release = "path/to/profile"

# (str) Comma-separated list of bundles to filter out when copying frameworks (eg. 'SystemConfiguration.framework')
#ios.framework_excludes = 

# (bool) Include debug symbols in the ipa bundle
#ios.include_debug_symbols = True

# (bool) Strip debug symbols from the ipa bundle
#ios.strip_debug_symbols = True

# (bool) Create a normal IPA instead of a debug one
#ios.create_release_ipa = False

# (str) The format of date to show to the user
#ios.date_format = "%Y-%m-%d"

# (str) Path to the root of the ios directory
#ios.codesign.allowed = false

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa)
bin_dir = ./bin

# (str) Path to the android SDK. This should be automatically set
export ANDROID_SDK_ROOT=./.buildozer/android/platform/android-sdk

# (str) Path to the android NDK. This should be automatically set
export ANDROID_NDK_HOME=./.buildozer/android/platform/android-ndk

# (str) Path to packages storage
export PACKAGES_PATH=./.buildozer/android/packages

# This is completed by buildozer automatically
#android.sdk = 31
