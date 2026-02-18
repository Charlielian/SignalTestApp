#!/usr/bin/env python3
"""
Python script to install and run SignalTestApp on Android devices

This script uses ADB (Android Debug Bridge) to:
1. Check if ADB is installed
2. Detect connected Android devices
3. Select a device if multiple are connected
4. Install the SignalTestApp APK
5. Launch the app
6. Verify installation
"""

import subprocess
import os
import sys
import time

# Constants
APP_PACKAGE = "com.signal.test"
APP_ACTIVITY = "com.signal.test.activities.MainActivity"
APK_PATH = "../SignalTestApp/app/build/intermediates/apk/debug/app-debug.apk"

def run_command(cmd, capture_output=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=capture_output,
            text=True,
            check=False
        )
        return result
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def check_adb_installed():
    """Check if ADB is installed and accessible"""
    print("Checking if ADB is installed...")
    result = run_command("adb version")
    if result and result.returncode == 0:
        print("✓ ADB is installed")
        return True
    else:
        print("✗ ADB is not installed or not in PATH")
        print("Please install ADB and add it to your PATH")
        print("You can download ADB from the Android SDK Platform Tools")
        return False

def get_connected_devices():
    """Get list of connected Android devices"""
    print("\nChecking for connected devices...")
    result = run_command("adb devices")
    if not result:
        return []
    
    devices = []
    lines = result.stdout.strip().split('\n')[1:]  # Skip the first line
    
    for line in lines:
        if line.strip():
            device_info = line.strip().split('\t')
            if len(device_info) >= 2 and device_info[1] == 'device':
                devices.append(device_info[0])
    
    if devices:
        print(f"✓ Found {len(devices)} connected device(s):")
        for i, device in enumerate(devices, 1):
            print(f"  {i}. {device}")
    else:
        print("✗ No devices connected")
        print("Please connect an Android device via USB with USB debugging enabled")
    
    return devices

def select_device(devices):
    """Allow user to select a device if multiple are connected"""
    if len(devices) == 1:
        print(f"\nUsing device: {devices[0]}")
        return devices[0]
    
    while True:
        try:
            choice = input(f"\nSelect a device (1-{len(devices)}): ")
            index = int(choice) - 1
            if 0 <= index < len(devices):
                selected_device = devices[index]
                print(f"Using device: {selected_device}")
                return selected_device
            else:
                print(f"Please enter a number between 1 and {len(devices)}")
        except ValueError:
            print("Please enter a valid number")

def check_apk_exists():
    """Check if the APK file exists"""
    apk_full_path = os.path.abspath(APK_PATH)
    print(f"\nChecking for APK file at: {apk_full_path}")
    
    if os.path.exists(apk_full_path):
        print("✓ APK file found")
        return apk_full_path
    else:
        print("✗ APK file not found")
        print("Please ensure the app has been built successfully")
        print(f"Expected path: {apk_full_path}")
        return None

def install_app(device, apk_path):
    """Install the app on the selected device"""
    print(f"\nInstalling app on device {device}...")
    
    cmd = f"adb -s {device} install -r {apk_path}"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        if "Success" in result.stdout:
            print("✓ App installed successfully")
            return True
        else:
            print("✗ Installation failed")
            print(f"ADB output: {result.stdout}")
            return False
    else:
        print("✗ Installation failed")
        if result:
            print(f"Error: {result.stderr}")
        return False

def launch_app(device):
    """Launch the app on the selected device"""
    print(f"\nLaunching app on device {device}...")
    
    cmd = f"adb -s {device} shell am start -n {APP_PACKAGE}/{APP_ACTIVITY}"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        if "Starting: Intent" in result.stdout:
            print("✓ App launched successfully")
            return True
        else:
            print("✗ Failed to launch app")
            print(f"ADB output: {result.stdout}")
            return False
    else:
        print("✗ Failed to launch app")
        if result:
            print(f"Error: {result.stderr}")
        return False

def verify_installation(device):
    """Verify the app is installed"""
    print(f"\nVerifying app installation on device {device}...")
    
    cmd = f"adb -s {device} shell pm list packages | grep {APP_PACKAGE}"
    result = run_command(cmd)
    
    if result and result.returncode == 0 and APP_PACKAGE in result.stdout:
        print("✓ App is installed")
        return True
    else:
        print("✗ App is not installed")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("SignalTestApp Installer")
    print("=" * 60)
    
    # Check if ADB is installed
    if not check_adb_installed():
        sys.exit(1)
    
    # Get connected devices
    devices = get_connected_devices()
    if not devices:
        sys.exit(1)
    
    # Select device
    selected_device = select_device(devices)
    
    # Check if APK exists
    apk_path = check_apk_exists()
    if not apk_path:
        sys.exit(1)
    
    # Install app
    if not install_app(selected_device, apk_path):
        sys.exit(1)
    
    # Launch app
    if not launch_app(selected_device):
        sys.exit(1)
    
    # Verify installation
    verify_installation(selected_device)
    
    print("\n" + "=" * 60)
    print("Installation and launch completed successfully!")
    print("The SignalTestApp should now be running on your device.")
    print("=" * 60)

if __name__ == "__main__":
    main()
