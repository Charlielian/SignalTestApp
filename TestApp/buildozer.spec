[app]
title = TestApp
package.name = testapp
package.domain = com.test
source.dir = .
requirements = python3,kivy
android.permissions = INTERNET
version = 1.0

[buildozer]
log_level = 2
build_dir = ./.buildozer
bin_dir = ./bin
export ANDROID_SDK_ROOT=./.buildozer/android/platform/android-sdk
export ANDROID_NDK_HOME=./.buildozer/android/platform/android-ndk
export PACKAGES_PATH=./.buildozer/android/packages
