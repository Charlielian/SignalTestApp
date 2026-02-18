# SignalTestApp Python

A Python implementation of the SignalTestApp using Kivy, packaged for Android using Buildozer.

## Features

- Real-time mobile network signal data collection
- Camera functionality with signal info overlay
- GPS location services
- Data storage and export
- Signal strength visualization
- Batch testing capabilities
- 4G/5G network support

## Project Structure

```
SignalTestApp_Python/
├── src/
│   ├── main.py              # Main entry point
│   ├── signal_collector.py   # Signal data collection
│   ├── camera_utils.py       # Camera functionality
│   ├── location_service.py   # Location services
│   ├── storage_utils.py      # Data storage
│   ├── ui/
│   │   ├── main_screen.py    # Main dashboard
│   │   ├── camera_screen.py  # Camera interface
│   │   ├── history_screen.py # History view
│   │   └── chart_screen.py   # Signal analysis
│   └── models/
│       └── signal_data.py    # Signal data model
├── assets/                   # Image and icon assets
├── buildozer.spec            # Buildozer configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Setup

### Prerequisites
- Python 3.7+
- pip
- Virtual environment (recommended)
- Buildozer (for Android packaging)
- Android SDK and NDK (for Buildozer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SignalTestApp_Python
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Buildozer**
   ```bash
   pip install buildozer
   buildozer init
   ```

## Running the App

### On Desktop
```bash
python src/main.py
```

### On Android
```bash
buildozer android debug deploy run
```

## Buildozer Configuration

Edit `buildozer.spec` to configure your app settings, including:
- App name and version
- Package name
- Permissions
- Dependencies
- Android API levels

## Permissions

The app requires the following permissions:
- CAMERA
- ACCESS_FINE_LOCATION
- ACCESS_COARSE_LOCATION
- INTERNET
- WRITE_EXTERNAL_STORAGE
- READ_EXTERNAL_STORAGE

## Testing

Test the app on:
- Multiple Android devices
- Different Android versions
- Various network conditions

## Troubleshooting

### Buildozer Issues
- Ensure Android SDK and NDK are properly installed
- Check buildozer.spec for correct configuration
- Refer to Buildozer documentation for platform-specific issues

### Signal Data Collection
- Some devices may require additional permissions
- 5G support depends on device capabilities

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

[MIT License](LICENSE)
