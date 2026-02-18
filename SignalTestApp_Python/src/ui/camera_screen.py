# Camera screen UI module

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock

class CameraScreen(Screen):
    """Camera screen for taking photos with signal info overlay"""
    
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.camera_utils = None
        self.signal_collector = None
        self.location_service = None
        self.storage_utils = None
        
        # Create layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add header
        self.header = BoxLayout(size_hint_y=0.1)
        self.title_label = Label(text='Camera', font_size='24sp', bold=True)
        self.header.add_widget(self.title_label)
        self.layout.add_widget(self.header)
        
        # Add camera preview area
        self.camera_layout = BoxLayout(size_hint_y=0.7)
        
        # Camera preview placeholder
        self.camera_preview = Image(source='', allow_stretch=True, keep_ratio=False)
        self.camera_layout.add_widget(self.camera_preview)
        
        self.layout.add_widget(self.camera_layout)
        
        # Add photo preview area
        self.photo_preview_layout = BoxLayout(size_hint_y=0.15)
        self.photo_preview = Image(source='', allow_stretch=True, keep_ratio=True)
        self.photo_preview_layout.add_widget(self.photo_preview)
        self.layout.add_widget(self.photo_preview_layout)
        
        # Add status label
        self.status_label = Label(text='Ready to take photo', size_hint_y=0.05)
        self.layout.add_widget(self.status_label)
        
        # Add buttons
        self.button_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        self.back_button = Button(text='Back', on_press=self.go_back)
        self.take_photo_button = Button(text='Take Photo', on_press=self.take_photo)
        self.view_photos_button = Button(text='View Photos', on_press=self.view_photos)
        
        self.button_layout.add_widget(self.back_button)
        self.button_layout.add_widget(self.take_photo_button)
        self.button_layout.add_widget(self.view_photos_button)
        
        self.layout.add_widget(self.button_layout)
        
        # Add layout to screen
        self.add_widget(self.layout)
        
        # Initialize camera
        self._initialize_camera()
    
    def _initialize_camera(self):
        """Initialize camera"""
        if self.camera_utils:
            success = self.camera_utils.initialize_camera()
            if success:
                self.camera = self.camera_utils.camera
                if self.camera:
                    # Add camera to preview
                    self.camera_layout.clear_widgets()
                    self.camera_layout.add_widget(self.camera)
                    self.status_label.text = 'Camera initialized'
                else:
                    self.status_label.text = 'Failed to get camera'
            else:
                self.status_label.text = 'Failed to initialize camera'
        else:
            self.status_label.text = 'Camera utilities not available'
    
    def take_photo(self, *args):
        """Take photo with signal info overlay"""
        if not self.camera_utils:
            self.status_label.text = 'Camera utilities not available'
            return
        
        if not self.camera_utils.camera:
            self.status_label.text = 'Camera not initialized'
            return
        
        # Get current signal data
        signal_data = None
        if self.signal_collector:
            signal_data = self.signal_collector.get_signal_data()
            
            if self.location_service:
                self.location_service.update_signal_data_location(signal_data)
        
        if not signal_data:
            self.status_label.text = 'Failed to get signal data'
            return
        
        # Take photo
        photo_path = self.camera_utils.take_photo(signal_data)
        
        if photo_path:
            self.status_label.text = f'Photo saved: {photo_path}'
            
            # Update photo preview
            self.photo_preview.source = photo_path
            self.photo_preview.reload()
            
            # Save signal data with photo path
            if self.storage_utils:
                self.storage_utils.insert_signal_data(signal_data)
                self.status_label.text += ' (Data saved)'
        else:
            self.status_label.text = 'Failed to take photo'
    
    def view_photos(self, *args):
        """View saved photos"""
        if self.camera_utils:
            photos = self.camera_utils.get_photo_list()
            if photos:
                self.status_label.text = f'Found {len(photos)} photos'
                # For now, just show the latest photo
                latest_photo = photos[0]
                self.photo_preview.source = latest_photo['path']
                self.photo_preview.reload()
            else:
                self.status_label.text = 'No photos found'
        else:
            self.status_label.text = 'Camera utilities not available'
    
    def go_back(self, *args):
        """Go back to main screen"""
        if self.manager:
            self.manager.current = 'main'
