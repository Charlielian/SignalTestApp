# History screen UI module

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.lang import Builder

# Kivy language definition for history item
Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.5, .5, .3) if self.selected else (0, 0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size
''')

class SelectableLabel(RecycleDataViewBehavior, Label):
    """Selectable label for recycle view"""
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    
    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle view changes"""
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)
    
    def on_touch_down(self, touch):
        """Add selection on touch down"""
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
    
    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view"""
        self.selected = is_selected

class HistoryScreen(Screen):
    """History screen for viewing saved signal data"""
    
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.storage_utils = None
        
        # Create layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add header
        self.header = BoxLayout(size_hint_y=0.1)
        self.title_label = Label(text='History', font_size='24sp', bold=True)
        self.header.add_widget(self.title_label)
        self.layout.add_widget(self.header)
        
        # Add data count label
        self.count_label = Label(text='Loading data...', size_hint_y=0.05)
        self.layout.add_widget(self.count_label)
        
        # Add history list
        self.history_layout = BoxLayout(size_hint_y=0.7)
        
        # Create recycle view for history items
        self.recycle_view = RecycleView()
        self.recycle_view.viewclass = 'SelectableLabel'
        self.recycle_view.data = []
        
        # Create layout manager
        layout_manager = RecycleBoxLayout(
            orientation='vertical',
            default_size=(None, 40),
            default_size_hint=(1, None),
            size_hint_y=None
        )
        
        # Add layout manager to recycle view
        self.recycle_view.add_widget(layout_manager)
        self.recycle_view.layout_manager = layout_manager
        
        self.history_layout.add_widget(self.recycle_view)
        self.layout.add_widget(self.history_layout)
        
        # Add buttons
        self.button_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        self.back_button = Button(text='Back', on_press=self.go_back)
        self.refresh_button = Button(text='Refresh', on_press=self.load_history)
        self.export_button = Button(text='Export', on_press=self.export_data)
        self.clear_button = Button(text='Clear All', on_press=self.clear_all)
        
        self.button_layout.add_widget(self.back_button)
        self.button_layout.add_widget(self.refresh_button)
        self.button_layout.add_widget(self.export_button)
        self.button_layout.add_widget(self.clear_button)
        
        self.layout.add_widget(self.button_layout)
        
        # Add layout to screen
        self.add_widget(self.layout)
        
        # Load history data
        self.load_history()
    
    def load_history(self, *args):
        """Load history data"""
        if self.storage_utils:
            # Get signal data
            signal_data_list = self.storage_utils.get_signal_data(limit=100)
            count = self.storage_utils.get_signal_data_count()
            
            self.count_label.text = f'Total records: {count}'
            
            # Prepare data for recycle view
            data = []
            for signal_data in signal_data_list:
                # Create display text
                display_text = f"{signal_data.timestamp} | {signal_data.network_type} | {signal_data.operator} | "
                display_text += f"Signal: {signal_data.get_signal_strength()} dBm | "
                display_text += f"Location: {signal_data.location_description[:30]}..."
                
                data.append({'text': display_text})
            
            # Update recycle view
            self.recycle_view.data = data
            
        else:
            self.count_label.text = 'Storage utilities not available'
            self.recycle_view.data = [{'text': 'No data available'}]
    
    def export_data(self, *args):
        """Export data"""
        if self.storage_utils:
            # Export to CSV
            csv_path = self.storage_utils.export_to_csv()
            if csv_path:
                self.count_label.text = f'Exported to: {csv_path}'
            else:
                self.count_label.text = 'Failed to export data'
        else:
            self.count_label.text = 'Storage utilities not available'
    
    def clear_all(self, *args):
        """Clear all data"""
        if self.storage_utils:
            success = self.storage_utils.delete_all_data()
            if success:
                self.count_label.text = 'All data cleared'
                self.recycle_view.data = []
            else:
                self.count_label.text = 'Failed to clear data'
        else:
            self.count_label.text = 'Storage utilities not available'
    
    def go_back(self, *args):
        """Go back to main screen"""
        if self.manager:
            self.manager.current = 'main'
