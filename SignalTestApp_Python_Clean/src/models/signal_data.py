# Signal data model

class SignalData:
    """Signal data model to store all signal-related information"""
    
    def __init__(self):
        # Network information
        self.network_type = "Unknown"
        self.operator = "Unknown"
        
        # 4G/LTE parameters
        self.cgi = "N/A"
        self.frequency = 0
        self.band = "N/A"
        self.pci = 0
        self.rssi = 0
        self.sinr = 0
        
        # 5G parameters
        self.nr_cgi = "N/A"
        self.nr_frequency = 0
        self.nr_band = "N/A"
        self.rsrp = 0
        self.nr_pci = 0
        self.rsrq = 0
        
        # Location information
        self.latitude = 0.0
        self.longitude = 0.0
        self.location_description = "Unknown"
        
        # Timestamp
        self.timestamp = ""
        
        # Photo path (if any)
        self.photo_path = ""
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            "network_type": self.network_type,
            "operator": self.operator,
            "cgi": self.cgi,
            "frequency": self.frequency,
            "band": self.band,
            "pci": self.pci,
            "rssi": self.rssi,
            "sinr": self.sinr,
            "nr_cgi": self.nr_cgi,
            "nr_frequency": self.nr_frequency,
            "nr_band": self.nr_band,
            "rsrp": self.rsrp,
            "nr_pci": self.nr_pci,
            "rsrq": self.rsrq,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location_description": self.location_description,
            "timestamp": self.timestamp,
            "photo_path": self.photo_path
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        signal_data = cls()
        for key, value in data.items():
            if hasattr(signal_data, key):
                setattr(signal_data, key, value)
        return signal_data
    
    def get_signal_strength(self):
        """Get signal strength based on network type"""
        if self.network_type == "5G" and self.rsrp != 0:
            return self.rsrp
        elif self.rssi != 0:
            return self.rssi
        return 0
    
    def get_signal_quality(self):
        """Get signal quality description"""
        strength = self.get_signal_strength()
        
        if strength >= -70:
            return "Excellent"
        elif strength >= -80:
            return "Good"
        elif strength >= -90:
            return "Fair"
        elif strength >= -100:
            return "Poor"
        else:
            return "Very Poor"
