# Python Script for Android App Installation and Execution

## Overview
Create a Python script that can install and run the SignalTestApp on Android devices using ADB (Android Debug Bridge).

## Implementation Plan

### 1. Directory Structure
- Create `SignalTestApp_py` directory
- Create main script file: `install_and_run_app.py`
- Create requirements.txt file for dependencies

### 2. Script Features
- **Device Detection**: Automatically detect connected Android devices
- **ADB Management**: Check if ADB is installed and accessible
- **App Installation**: Install the debug APK from `SignalTestApp/app/build/intermediates/apk/debug/app-debug.apk`
- **App Launch**: Launch the SignalTestApp on the device
- **Error Handling**: Handle common ADB errors gracefully
- **Logging**: Provide clear output of operations

### 3. Dependencies
- Python 3.6+
- subprocess (standard library)
- os (standard library)
- sys (standard library)
- time (standard library)
- ADB (Android Debug Bridge) must be installed on the system

### 4. Script Functionality
1. **Check ADB Installation**: Verify ADB is available in PATH
2. **List Connected Devices**: Show all connected Android devices
3. **Select Device**: Allow user to select a device if multiple are connected
4. **Install App**: Push and install the APK file
5. **Launch App**: Start the app using its package name
6. **Verify Installation**: Confirm app is installed and running

### 5. Usage Instructions
- Ensure ADB is installed and added to PATH
- Connect Android device via USB with USB debugging enabled
- Run the script: `python install_and_run_app.py`
- Follow on-screen instructions

### 6. Error Handling
- Handle ADB not found error
- Handle no devices connected error
- Handle installation failures
- Provide clear error messages and troubleshooting steps

### 7. Testing
- Test script with multiple devices
- Test script with different Android versions
- Test error handling scenarios

## Expected Outcome
A reliable Python script that simplifies the process of installing and running the SignalTestApp on Android devices, making it easier for testing and development purposes.