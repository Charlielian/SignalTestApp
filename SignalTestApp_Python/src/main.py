# Main application entry point

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.config import Config
import os

# Set default font to support Chinese characters
# Use system fonts that are likely to support Chinese
Config.set('kivy', 'default_font', ['Arial Unicode MS', 'PingFang SC', 'Hiragino Sans GB', 'WenQuanYi Micro Hei', 'Arial', 'sans-serif'])

# Import screens
from ui.main_screen import MainScreen
from ui.camera_screen import CameraScreen
from ui.history_screen import HistoryScreen
from ui.chart_screen import ChartScreen

# Import services
from signal_collector import SignalCollector
from camera_utils import CameraUtils
from location_service import LocationService
from storage_utils import StorageUtils

class SignalTestApp(App):
    """Main application class"""
    
    def __init__(self, **kwargs):
        super(SignalTestApp, self).__init__(**kwargs)
        self.signal_collector = None
        self.camera_utils = None
        self.location_service = None
        self.storage_utils = None
        self.screen_manager = None
        self.android_context = None
    
    def build(self):
        """Build the application"""
        # Set window size for desktop
        Window.size = (800, 600)
        
        # Initialize services
        self._initialize_services()
        
        # Create screen manager
        self.screen_manager = ScreenManager()
        
        # Create screens
        main_screen = MainScreen(name='main')
        main_screen.signal_collector = self.signal_collector
        main_screen.location_service = self.location_service
        main_screen.storage_utils = self.storage_utils
        main_screen.camera_utils = self.camera_utils
        
        camera_screen = CameraScreen(name='camera')
        camera_screen.camera_utils = self.camera_utils
        camera_screen.signal_collector = self.signal_collector
        camera_screen.location_service = self.location_service
        camera_screen.storage_utils = self.storage_utils
        
        history_screen = HistoryScreen(name='history')
        history_screen.storage_utils = self.storage_utils
        
        chart_screen = ChartScreen(name='chart')
        chart_screen.storage_utils = self.storage_utils
        
        # Add screens to manager
        self.screen_manager.add_widget(main_screen)
        self.screen_manager.add_widget(camera_screen)
        self.screen_manager.add_widget(history_screen)
        self.screen_manager.add_widget(chart_screen)
        
        # Set initial screen
        self.screen_manager.current = 'main'
        
        return self.screen_manager
    
    def _initialize_services(self):
        """Initialize all services"""
        # Try to get Android context if running on Android
        self._get_android_context()
        
        # Initialize services
        self.signal_collector = SignalCollector(context=self.android_context)
        self.camera_utils = CameraUtils(app=self)
        self.location_service = LocationService(context=self.android_context)
        self.storage_utils = StorageUtils(app=self)
        
        print("Services initialized successfully")
    
    def _get_android_context(self):
        """Get Android context using PyJNIus"""
        try:
            from jnius import autoclass, cast
            
            # Get PythonActivity
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            current_activity = PythonActivity.mActivity
            
            if current_activity:
                self.android_context = current_activity
                print("Android context obtained successfully")
        except Exception as e:
            print(f"Error getting Android context: {e}")
            self.android_context = None
    
    def get_context(self):
        """Get Android context (for storage utils)"""
        return self.android_context
    
    def on_stop(self):
        """Handle app stop"""
        print("App stopping...")
        # Clean up resources if needed
        super(SignalTestApp, self).on_stop()

if __name__ == '__main__':
    # Run the application
    SignalTestApp().run()
