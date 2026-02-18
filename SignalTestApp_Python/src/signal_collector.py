# Signal data collection module

import platform
from datetime import datetime

class SignalCollector:
    """Collect mobile network signal data"""
    
    def __init__(self, context=None):
        self.context = context
        self.is_android = platform.system() == 'Android'
        self.telephony_manager = None
        
        if self.is_android and context:
            self._init_android_telephony_manager()
    
    def _init_android_telephony_manager(self):
        """Initialize Android TelephonyManager using PyJNIus"""
        try:
            from jnius import autoclass
            
            # Get TelephonyManager
            TelephonyManager = autoclass('android.telephony.TelephonyManager')
            Context = autoclass('android.content.Context')
            
            self.telephony_manager = self.context.getSystemService(Context.TELEPHONY_SERVICE)
        except Exception as e:
            print(f"Error initializing TelephonyManager: {e}")
            self.telephony_manager = None
    
    def get_signal_data(self):
        """Get signal data based on platform"""
        from models.signal_data import SignalData
        
        signal_data = SignalData()
        signal_data.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if self.is_android and self.telephony_manager:
            self._collect_android_signal_data(signal_data)
        else:
            # For non-Android platforms, return mock data
            self._collect_mock_signal_data(signal_data)
        
        return signal_data
    
    def _collect_android_signal_data(self, signal_data):
        """Collect signal data on Android"""
        try:
            from jnius import autoclass
            
            # Get network type
            network_type = self.telephony_manager.getNetworkType()
            signal_data.network_type = self._get_network_type_string(network_type)
            
            # Get operator info
            signal_data.operator = self.telephony_manager.getNetworkOperatorName() or "Unknown"
            
            # Get cell info (requires Android 17+)
            if hasattr(self.telephony_manager, 'getAllCellInfo'):
                cell_info_list = self.telephony_manager.getAllCellInfo()
                if cell_info_list:
                    self._process_cell_info(cell_info_list, signal_data)
                    
        except Exception as e:
            print(f"Error collecting Android signal data: {e}")
            # Fall back to mock data
            self._collect_mock_signal_data(signal_data)
    
    def _process_cell_info(self, cell_info_list, signal_data):
        """Process cell info list"""
        try:
            from jnius import autoclass
            
            CellInfoLte = autoclass('android.telephony.CellInfoLte')
            CellInfoNr = autoclass('android.telephony.CellInfoNr')
            CellIdentityLte = autoclass('android.telephony.CellIdentityLte')
            CellIdentityNr = autoclass('android.telephony.CellIdentityNr')
            CellSignalStrengthLte = autoclass('android.telephony.CellSignalStrengthLte')
            CellSignalStrengthNr = autoclass('android.telephony.CellSignalStrengthNr')
            
            for cell_info in cell_info_list:
                if cell_info and cell_info.isRegistered():
                    if isinstance(cell_info, CellInfoLte):
                        # Process LTE (4G) info
                        cell_identity = cell_info.getCellIdentity()
                        cell_signal = cell_info.getCellSignalStrength()
                        
                        if cell_identity:
                            # Format CGI as 460-00-123245678-1
                            mcc = cell_identity.getMcc()
                            mnc = cell_identity.getMnc()
                            tac = cell_identity.getTac()
                            ci = cell_identity.getCi()
                            signal_data.cgi = f"{mcc}-{mnc}-{tac}-{ci}"
                            signal_data.frequency = cell_identity.getEarfcn()
                            signal_data.band = self._get_lte_band(cell_identity.getEarfcn())
                            signal_data.pci = cell_identity.getPci()
                        
                        if cell_signal:
                            signal_data.rssi = cell_signal.getRssi()
                            signal_data.sinr = cell_signal.getSinr()
                            
                    elif isinstance(cell_info, CellInfoNr):
                        # Process NR (5G) info
                        cell_identity = cell_info.getCellIdentity()
                        cell_signal = cell_info.getCellSignalStrength()
                        
                        if cell_identity:
                            # Format NR CGI as 460-00-123245678-1
                            mcc = cell_identity.getMcc()
                            mnc = cell_identity.getMnc()
                            tac = cell_identity.getTac()
                            nci = cell_identity.getNci()
                            signal_data.nr_cgi = f"{mcc}-{mnc}-{tac}-{nci}"
                            signal_data.nr_frequency = cell_identity.getNrarfcn()
                            signal_data.nr_band = self._get_5g_band(cell_identity.getNrarfcn())
                            signal_data.nr_pci = cell_identity.getPci()
                        
                        if cell_signal:
                            signal_data.rsrp = cell_signal.getRsrp()
                            signal_data.rsrq = cell_signal.getRsrq()
                            # Set network type to 5G if we have 5G info
                            signal_data.network_type = "5G"
        
        except Exception as e:
            print(f"Error processing cell info: {e}")
    
    def _collect_mock_signal_data(self, signal_data):
        """Collect mock signal data for non-Android platforms"""
        signal_data.network_type = "4G"
        signal_data.operator = "China Mobile"
        # Format CGI as 460-00-123245678-1
        signal_data.cgi = "460-00-12345678-90"
        signal_data.frequency = 1850
        signal_data.band = "Band 3"
        signal_data.pci = 123
        signal_data.rssi = -75
        signal_data.sinr = 25
        # Format NR CGI as 460-00-123245678-1
        signal_data.nr_cgi = "460-00-12345678-90"
        signal_data.nr_frequency = 0
        signal_data.nr_band = "N/A"
        signal_data.rsrp = 0
        signal_data.nr_pci = 0
        signal_data.rsrq = 0
    
    def _get_network_type_string(self, network_type):
        """Convert network type integer to string"""
        network_types = {
            1: "2G",  # GPRS
            2: "2G",  # EDGE
            3: "3G",  # UMTS
            8: "3G",  # HSDPA
            9: "3G",  # HSUPA
            10: "3G", # HSPA
            13: "4G", # LTE
            20: "5G"  # NR
        }
        return network_types.get(network_type, "Unknown")
    
    def _get_lte_band(self, earfcn):
        """Get LTE band from EARFCN"""
        # Simplified band mapping
        if 1 <= earfcn <= 599:
            return "Band 1"
        elif 600 <= earfcn <= 1199:
            return "Band 2"
        elif 1200 <= earfcn <= 1949:
            return "Band 3"
        elif 1950 <= earfcn <= 2399:
            return "Band 4"
        elif 2400 <= earfcn <= 2649:
            return "Band 5"
        else:
            return f"Band {earfcn//1000}"
    
    def _get_5g_band(self, nrarfcn):
        """Get 5G band from NRARFCN"""
        # Simplified band mapping
        if 0 <= nrarfcn <= 299999:
            return "n77"
        elif 300000 <= nrarfcn <= 699999:
            return "n78"
        elif 700000 <= nrarfcn <= 899999:
            return "n79"
        else:
            return f"n{ nrarfcn//100000 }"
    
    def set_network_type(self, network_type):
        """Set preferred network type
        
        Args:
            network_type (str): Network type to set, one of "2G", "3G", "4G", "5G"
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_android or not self.telephony_manager:
            print("Network type control not available on this platform")
            return False
        
        try:
            from jnius import autoclass
            
            # Get network type constants
            TelephonyManager = autoclass('android.telephony.TelephonyManager')
            
            # Map network type string to constant
            network_type_map = {
                "2G": TelephonyManager.NETWORK_TYPE_GSM,
                "3G": TelephonyManager.NETWORK_TYPE_UMTS,
                "4G": TelephonyManager.NETWORK_TYPE_LTE,
                "5G": TelephonyManager.NETWORK_TYPE_NR
            }
            
            if network_type not in network_type_map:
                print(f"Invalid network type: {network_type}")
                return False
            
            # Set preferred network type
            # Note: This requires MODIFY_PHONE_STATE permission
            if hasattr(self.telephony_manager, 'setPreferredNetworkType'):
                self.telephony_manager.setPreferredNetworkType(network_type_map[network_type])
                print(f"Preferred network type set to {network_type}")
                return True
            else:
                print("setPreferredNetworkType not available on this device")
                return False
                
        except Exception as e:
            print(f"Error setting network type: {e}")
            return False
