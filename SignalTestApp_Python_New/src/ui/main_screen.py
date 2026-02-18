# Main screen UI module

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class MainScreen(Screen):
    """Main dashboard screen showing signal information"""
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.signal_collector = None
        self.location_service = None
        self.storage_utils = None
        self.camera_utils = None
        
        # Create layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add header with network type control
        self.header = BoxLayout(size_hint_y=0.1, spacing=10)
        self.title_label = Label(text='Signal Test App', font_size='24sp', bold=True, size_hint_x=0.6)
        
        # Add network type toggle switch to header (top left)
        self.network_control_layout = BoxLayout(size_hint_x=0.4, spacing=5)
        self.network_control_label = Label(text='Network:', size_hint_x=0.3)
        
        # Create toggle switch for 4G/5G
        self.network_toggle_layout = BoxLayout(size_hint_x=0.7, orientation='horizontal')
        
        # Create toggle background
        self.toggle_background = BoxLayout(size_hint=(1, 1), padding=2)
        self.toggle_background.canvas.before.clear()
        with self.toggle_background.canvas.before:
            Color(0.3, 0.3, 0.3, 1)
            Rectangle(pos=self.toggle_background.pos, size=self.toggle_background.size)
        
        # Create toggle buttons
        self.network_toggle_4g = Button(text='4G', on_press=lambda x: self.set_network_type('4G'), 
                                       background_color=(0, 0.7, 0.7, 1), 
                                       size_hint_x=0.5, 
                                       bold=True)
        self.network_toggle_5g = Button(text='5G', on_press=lambda x: self.set_network_type('5G'), 
                                       background_color=(0.5, 0.5, 0.5, 1), 
                                       size_hint_x=0.5)
        
        self.toggle_background.add_widget(self.network_toggle_4g)
        self.toggle_background.add_widget(self.network_toggle_5g)
        self.network_toggle_layout.add_widget(self.toggle_background)
        
        self.network_control_layout.add_widget(self.network_control_label)
        self.network_control_layout.add_widget(self.network_toggle_layout)
        
        self.header.add_widget(self.network_control_layout)
        self.header.add_widget(self.title_label)
        self.layout.add_widget(self.header)
        
        # Add signal info grid
        self.signal_info_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.6)
        
        # Create signal info labels
        self.network_type_label = self._create_info_label('Network Type', 'network_type')
        self.operator_label = self._create_info_label('Operator', 'operator')
        self.signal_strength_label = self._create_info_label('Signal Strength', 'signal_strength')
        self.signal_quality_label = self._create_info_label('Signal Quality', 'signal_quality')
        self.cgi_label = self._create_info_label('CGI', 'cgi')
        self.pci_label = self._create_info_label('PCI', 'pci')
        self.band_label = self._create_info_label('Band', 'band')
        self.frequency_label = self._create_info_label('Frequency', 'frequency')
        self.location_label = self._create_info_label('Location', 'location')
        self.timestamp_label = self._create_info_label('Timestamp', 'timestamp')
        
        # Add labels to grid
        self.signal_info_layout.add_widget(self.network_type_label)
        self.signal_info_layout.add_widget(self.operator_label)
        self.signal_info_layout.add_widget(self.signal_strength_label)
        self.signal_info_layout.add_widget(self.signal_quality_label)
        self.signal_info_layout.add_widget(self.cgi_label)
        self.signal_info_layout.add_widget(self.pci_label)
        self.signal_info_layout.add_widget(self.band_label)
        self.signal_info_layout.add_widget(self.frequency_label)
        self.signal_info_layout.add_widget(self.location_label)
        self.signal_info_layout.add_widget(self.timestamp_label)
        
        # Add scroll view for signal info
        self.scroll_view = ScrollView(size_hint_y=0.6)
        self.scroll_view.add_widget(self.signal_info_layout)
        self.layout.add_widget(self.scroll_view)
        
        # Add action buttons
        self.button_layout = GridLayout(cols=3, spacing=10, size_hint_y=0.2)
        
        self.camera_button = Button(text='Camera', on_press=self.go_to_camera)
        self.history_button = Button(text='History', on_press=self.go_to_history)
        self.chart_button = Button(text='Chart', on_press=self.go_to_chart)
        self.save_button = Button(text='Save', on_press=self.save_data)
        self.export_button = Button(text='Export', on_press=self.export_data)
        self.refresh_button = Button(text='Refresh', on_press=self.update_signal_info)
        
        self.button_layout.add_widget(self.camera_button)
        self.button_layout.add_widget(self.history_button)
        self.button_layout.add_widget(self.chart_button)
        self.button_layout.add_widget(self.save_button)
        self.button_layout.add_widget(self.export_button)
        self.button_layout.add_widget(self.refresh_button)
        
        self.layout.add_widget(self.button_layout)
        
        # Add layout to screen
        self.add_widget(self.layout)
        
        # Start periodic update
        Clock.schedule_interval(self.update_signal_info, 5)  # Update every 5 seconds
    
    def _create_info_label(self, title, attr_name):
        """Create info label with title"""
        layout = BoxLayout(orientation='vertical', padding=5)
        title_label = Label(text=title, font_size='14sp', bold=True, size_hint_y=0.3)
        value_label = Label(text='N/A', font_size='16sp', size_hint_y=0.7)
        layout.add_widget(title_label)
        layout.add_widget(value_label)
        
        # Store reference to value label
        setattr(self, f'{attr_name}_value', value_label)
        
        return layout
    
    def update_signal_info(self, *args):
        """Update signal information"""
        if self.signal_collector:
            signal_data = self.signal_collector.get_signal_data()
            
            if self.location_service:
                self.location_service.update_signal_data_location(signal_data)
            
            # Update labels
            self.network_type_value.text = signal_data.network_type
            self.operator_value.text = signal_data.operator
            self.signal_strength_value.text = f"{signal_data.get_signal_strength()} dBm"
            self.signal_quality_value.text = signal_data.get_signal_quality()
            
            # Use 5G values if available
            if signal_data.network_type == "5G":
                self.cgi_value.text = signal_data.nr_cgi
                self.pci_value.text = str(signal_data.nr_pci) if signal_data.nr_pci != 0 else "N/A"
                self.band_value.text = signal_data.nr_band
                self.frequency_value.text = str(signal_data.nr_frequency) if signal_data.nr_frequency != 0 else "N/A"
            else:
                self.cgi_value.text = signal_data.cgi
                self.pci_value.text = str(signal_data.pci) if signal_data.pci != 0 else "N/A"
                self.band_value.text = signal_data.band
                self.frequency_value.text = str(signal_data.frequency) if signal_data.frequency != 0 else "N/A"
            
            self.location_value.text = signal_data.location_description
            self.timestamp_value.text = signal_data.timestamp
            
            # Store current signal data for saving
            self.current_signal_data = signal_data
    
    def save_data(self, *args):
        """Save current signal data"""
        if hasattr(self, 'current_signal_data') and self.storage_utils:
            success = self.storage_utils.insert_signal_data(self.current_signal_data)
            if success:
                print("Data saved successfully")
                # Show feedback to user
                self.timestamp_value.text = f"{self.current_signal_data.timestamp} (Saved)"
            else:
                print("Failed to save data")
    
    def export_data(self, *args):
        """Export data"""
        if self.storage_utils:
            csv_path = self.storage_utils.export_to_csv()
            if csv_path:
                print(f"Data exported to: {csv_path}")
                # Show feedback to user
                self.timestamp_value.text = f"Exported to CSV"
    
    def go_to_camera(self, *args):
        """Go to camera screen"""
        if self.manager:
            self.manager.current = 'camera'
    
    def go_to_history(self, *args):
        """Go to history screen"""
        if self.manager:
            self.manager.current = 'history'
    
    def go_to_chart(self, *args):
        """Go to chart screen"""
        if self.manager:
            self.manager.current = 'chart'
    
    def set_network_type(self, network_type):
        """Set network type (4G or 5G)"""
        # Update toggle switch UI
        if network_type == '4G':
            self.network_toggle_4g.background_color = (0, 0.7, 0.7, 1)  # Highlight 4G
            self.network_toggle_4g.bold = True
            self.network_toggle_5g.background_color = (0.5, 0.5, 0.5, 1)  # Dim 5G
            self.network_toggle_5g.bold = False
        elif network_type == '5G':
            self.network_toggle_4g.background_color = (0.5, 0.5, 0.5, 1)  # Dim 4G
            self.network_toggle_4g.bold = False
            self.network_toggle_5g.background_color = (0, 0.7, 0.7, 1)  # Highlight 5G
            self.network_toggle_5g.bold = True
        
        # Call signal collector to set network type
        if self.signal_collector:
            success = self.signal_collector.set_network_type(network_type)
            if success:
                print(f"Network type set to {network_type}")
                # Update signal info after changing network type
                self.update_signal_info()
            else:
                print(f"Failed to set network type to {network_type}")
        else:
            print("Signal collector not available")
