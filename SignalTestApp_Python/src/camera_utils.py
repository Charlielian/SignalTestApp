# Camera functionality module

import os
import platform
from datetime import datetime
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage
from PIL import Image, ImageDraw, ImageFont

class CameraUtils:
    """Camera utilities for taking photos and overlaying signal info"""
    
    def __init__(self, app=None):
        self.app = app
        self.camera = None
        self.is_android = platform.system() == 'Android'
        self.photo_directory = self._get_photo_directory()
    
    def _get_photo_directory(self):
        """Get directory for storing photos"""
        if self.is_android:
            # On Android, use external storage
            try:
                from jnius import autoclass
                Environment = autoclass('android.os.Environment')
                app_dir = os.path.join(
                    Environment.getExternalStorageDirectory().getAbsolutePath(),
                    'SignalTestApp'
                )
            except Exception:
                app_dir = 'photos'
        else:
            # On other platforms, use local directory
            app_dir = 'photos'
        
        # Create directory if it doesn't exist
        os.makedirs(app_dir, exist_ok=True)
        return app_dir
    
    def initialize_camera(self):
        """Initialize camera"""
        try:
            from kivy.uix.camera import Camera
            self.camera = Camera(play=True, resolution=(640, 480))
            return True
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def take_photo(self, signal_data):
        """Take photo and overlay signal information"""
        if not self.camera:
            print("Camera not initialized")
            return None
        
        try:
            # Get current time for filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"signal_test_{timestamp}.jpg"
            filepath = os.path.join(self.photo_directory, filename)
            
            # Take photo
            texture = self.camera.texture
            if texture:
                # Save texture to image
                pixels = texture.pixels
                size = texture.size
                
                # Create PIL image
                image = Image.frombytes('RGBA', size, pixels)
                image = image.convert('RGB')  # Convert to RGB
                
                # Overlay signal information
                self._overlay_signal_info(image, signal_data)
                
                # Save image
                image.save(filepath)
                print(f"Photo saved to: {filepath}")
                
                # Update signal data with photo path
                signal_data.photo_path = filepath
                
                return filepath
            else:
                print("No camera texture available")
                return None
                
        except Exception as e:
            print(f"Error taking photo: {e}")
            return None
    
    def _overlay_signal_info(self, image, signal_data):
        """Overlay signal information on image"""
        try:
            draw = ImageDraw.Draw(image)
            
            # Try to load a font, fallback to default if not available
            try:
                font = ImageFont.truetype('arial', 12)
            except Exception:
                font = ImageFont.load_default()
            
            # Prepare signal info text
            info_lines = [
                f"Network: {signal_data.network_type}",
                f"Operator: {signal_data.operator}",
                f"Signal: {signal_data.get_signal_strength()} dBm",
                f"Quality: {signal_data.get_signal_quality()}",
                f"PCI: {signal_data.pci or signal_data.nr_pci}",
                f"Band: {signal_data.band or signal_data.nr_band}",
                f"Location: {signal_data.location_description}",
                f"Time: {signal_data.timestamp}"
            ]
            
            # Calculate text position (bottom left corner)
            x = 10
            y = image.height - 10 - len(info_lines) * 15
            
            # Draw semi-transparent background
            box_height = len(info_lines) * 15 + 10
            box_width = max([draw.textlength(line, font=font) for line in info_lines]) + 20
            
            # Draw background rectangle
            draw.rectangle(
                [(x-5, y-5), (x + box_width, y + box_height)],
                fill=(0, 0, 0, 128)
            )
            
            # Draw text
            for i, line in enumerate(info_lines):
                draw.text(
                    (x, y + i * 15),
                    line,
                    font=font,
                    fill=(255, 255, 255)
                )
                
        except Exception as e:
            print(f"Error overlaying signal info: {e}")
    
    def get_photo_preview(self, photo_path):
        """Get photo preview texture"""
        try:
            if os.path.exists(photo_path):
                image = CoreImage(photo_path)
                return image.texture
            return None
        except Exception as e:
            print(f"Error getting photo preview: {e}")
            return None
    
    def get_photo_list(self):
        """Get list of saved photos"""
        try:
            photos = []
            for file in os.listdir(self.photo_directory):
                if file.lower().endswith('.jpg'):
                    filepath = os.path.join(self.photo_directory, file)
                    photos.append({
                        'filename': file,
                        'path': filepath,
                        'timestamp': os.path.getmtime(filepath)
                    })
            
            # Sort by timestamp (newest first)
            photos.sort(key=lambda x: x['timestamp'], reverse=True)
            return photos
        except Exception as e:
            print(f"Error getting photo list: {e}")
            return []
    
    def delete_photo(self, photo_path):
        """Delete photo"""
        try:
            if os.path.exists(photo_path):
                os.remove(photo_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting photo: {e}")
            return False
