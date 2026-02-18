# Chart screen UI module

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import numpy as np

class ChartScreen(Screen):
    """Chart screen for signal strength visualization"""
    
    def __init__(self, **kwargs):
        super(ChartScreen, self).__init__(**kwargs)
        self.storage_utils = None
        
        # Create layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add header
        self.header = BoxLayout(size_hint_y=0.1)
        self.title_label = Label(text='Signal Analysis', font_size='24sp', bold=True)
        self.header.add_widget(self.title_label)
        self.layout.add_widget(self.header)
        
        # Add chart area
        self.chart_layout = BoxLayout(size_hint_y=0.7)
        
        # Create initial placeholder
        self.placeholder_label = Label(text='Chart functionality disabled', font_size='16sp')
        self.chart_layout.add_widget(self.placeholder_label)
        
        self.layout.add_widget(self.chart_layout)
        
        # Add buttons
        self.button_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        self.back_button = Button(text='Back', on_press=self.go_back)
        self.refresh_button = Button(text='Refresh', on_press=self.update_chart)
        self.signal_strength_button = Button(text='Signal Strength', on_press=self.show_signal_strength)
        self.network_type_button = Button(text='Network Type', on_press=self.show_network_type)
        
        self.button_layout.add_widget(self.back_button)
        self.button_layout.add_widget(self.refresh_button)
        self.button_layout.add_widget(self.signal_strength_button)
        self.button_layout.add_widget(self.network_type_button)
        
        self.layout.add_widget(self.button_layout)
        
        # Add status label
        self.status_label = Label(text='Chart functionality disabled', size_hint_y=0.05)
        self.layout.add_widget(self.status_label)
        
        # Add layout to screen
        self.add_widget(self.layout)
        
        # Initial chart type
        self.current_chart_type = 'signal_strength'
    
    def update_chart(self, *args):
        """Update chart based on current chart type"""
        self.status_label.text = 'Chart functionality disabled'
    
    def show_signal_strength(self, *args):
        """Show signal strength chart"""
        self.current_chart_type = 'signal_strength'
        self.status_label.text = 'Signal Strength chart disabled'
    
    def show_network_type(self, *args):
        """Show network type distribution chart"""
        self.current_chart_type = 'network_type'
        self.status_label.text = 'Network Type chart disabled'
    
    def go_back(self, *args):
        """Go back to main screen"""
        if self.manager:
            self.manager.current = 'main'
