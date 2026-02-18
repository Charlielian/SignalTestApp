# Location services module

import platform
import requests

class LocationService:
    """Location services for GPS and geocoding"""
    
    def __init__(self, context=None):
        self.context = context
        self.is_android = platform.system() == 'Android'
        self.location_manager = None
        self.last_location = None
        
        if self.is_android and context:
            self._init_android_location_manager()
    
    def _init_android_location_manager(self):
        """Initialize Android LocationManager using PyJNIus"""
        try:
            from jnius import autoclass
            
            # Get LocationManager
            LocationManager = autoclass('android.location.LocationManager')
            Context = autoclass('android.content.Context')
            
            self.location_manager = self.context.getSystemService(Context.LOCATION_SERVICE)
        except Exception as e:
            print(f"Error initializing LocationManager: {e}")
            self.location_manager = None
    
    def get_location(self):
        """Get current location"""
        if self.is_android and self.location_manager:
            return self._get_android_location()
        else:
            # For non-Android platforms, return mock location
            return self._get_mock_location()
    
    def _get_android_location(self):
        """Get location on Android"""
        try:
            from jnius import autoclass
            
            # Check for location permissions
            if not self._has_location_permission():
                print("Location permission not granted")
                return self._get_mock_location()
            
            # Get last known location
            providers = ['gps', 'network']
            location = None
            
            for provider in providers:
                try:
                    if self.location_manager.isProviderEnabled(provider):
                        location = self.location_manager.getLastKnownLocation(provider)
                        if location:
                            break
                except Exception as e:
                    print(f"Error getting location from {provider}: {e}")
            
            if location:
                latitude = location.getLatitude()
                longitude = location.getLongitude()
                self.last_location = (latitude, longitude)
                return {
                    'latitude': latitude,
                    'longitude': longitude,
                    'accuracy': location.getAccuracy() if hasattr(location, 'getAccuracy') else 0
                }
            else:
                print("No location available")
                return self._get_mock_location()
                
        except Exception as e:
            print(f"Error getting Android location: {e}")
            return self._get_mock_location()
    
    def _has_location_permission(self):
        """Check if location permission is granted"""
        try:
            from jnius import autoclass
            
            ContextCompat = autoclass('androidx.core.content.ContextCompat')
            Manifest = autoclass('android.Manifest')
            
            fine_location_perm = Manifest.permission.ACCESS_FINE_LOCATION
            coarse_location_perm = Manifest.permission.ACCESS_COARSE_LOCATION
            
            fine_granted = ContextCompat.checkSelfPermission(
                self.context, fine_location_perm
            ) == 0  # 0 is PERMISSION_GRANTED
            
            coarse_granted = ContextCompat.checkSelfPermission(
                self.context, coarse_location_perm
            ) == 0
            
            return fine_granted or coarse_granted
            
        except Exception as e:
            print(f"Error checking location permission: {e}")
            return False
    
    def _get_mock_location(self):
        """Get mock location for non-Android platforms"""
        return {
            'latitude': 39.9042,
            'longitude': 116.4074,
            'accuracy': 10
        }
    
    def get_location_description(self, latitude=None, longitude=None):
        """Get human-readable location description"""
        if not latitude or not longitude:
            location = self.get_location()
            latitude = location['latitude']
            longitude = location['longitude']
        
        # Try to get address from coordinates
        address = self._reverse_geocode(latitude, longitude)
        if address:
            return address
        else:
            # Fallback to coordinates
            return f"{latitude:.6f}, {longitude:.6f}"
    
    def _reverse_geocode(self, latitude, longitude):
        """Reverse geocode coordinates to address"""
        try:
            # Use OpenStreetMap Nominatim API
            url = f"https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json',
                'zoom': 16,
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'SignalTestApp/1.0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'display_name' in data:
                    return data['display_name']
        except Exception as e:
            print(f"Error reverse geocoding: {e}")
        
        return None
    
    def update_signal_data_location(self, signal_data):
        """Update signal data with location information"""
        location = self.get_location()
        signal_data.latitude = location['latitude']
        signal_data.longitude = location['longitude']
        signal_data.location_description = self.get_location_description(
            location['latitude'], location['longitude']
        )
        return signal_data
