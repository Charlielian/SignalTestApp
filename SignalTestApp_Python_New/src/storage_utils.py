# Data storage and export module

import os
import sqlite3
import platform
import pandas as pd
from datetime import datetime

class StorageUtils:
    """Storage utilities for SQLite and data export"""
    
    def __init__(self, app=None):
        self.app = app
        self.db_path = self._get_db_path()
        self._init_database()
    
    def _get_db_path(self):
        """Get database path based on platform"""
        if platform.system() == 'Android':
            # On Android, use app data directory
            try:
                from jnius import autoclass
                Context = autoclass('android.content.Context')
                Environment = autoclass('android.os.Environment')
                
                # Get external files directory
                if self.app and hasattr(self.app, 'get_context'):
                    context = self.app.get_context()
                    db_dir = context.getExternalFilesDir(None).getAbsolutePath()
                else:
                    db_dir = Environment.getExternalStorageDirectory().getAbsolutePath()
            except Exception:
                db_dir = '.'
        else:
            # On other platforms, use local directory
            db_dir = '.'
        
        # Create directory if it doesn't exist
        os.makedirs(db_dir, exist_ok=True)
        return os.path.join(db_dir, 'signal_test.db')
    
    def _init_database(self):
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create signal_data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS signal_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    network_type TEXT,
                    operator TEXT,
                    cgi TEXT,
                    frequency INTEGER,
                    band TEXT,
                    pci INTEGER,
                    rssi INTEGER,
                    sinr INTEGER,
                    nr_cgi TEXT,
                    nr_frequency INTEGER,
                    nr_band TEXT,
                    rsrp INTEGER,
                    nr_pci INTEGER,
                    rsrq INTEGER,
                    latitude REAL,
                    longitude REAL,
                    location_description TEXT,
                    timestamp TEXT,
                    photo_path TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            print(f"Database initialized at: {self.db_path}")
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def insert_signal_data(self, signal_data):
        """Insert signal data into database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert signal data to dict
            data = signal_data.to_dict()
            
            # Insert data
            cursor.execute('''
                INSERT INTO signal_data (
                    network_type, operator, cgi, frequency, band, pci, rssi, sinr,
                    nr_cgi, nr_frequency, nr_band, rsrp, nr_pci, rsrq,
                    latitude, longitude, location_description, timestamp, photo_path
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', (
                data['network_type'], data['operator'], data['cgi'], data['frequency'],
                data['band'], data['pci'], data['rssi'], data['sinr'],
                data['nr_cgi'], data['nr_frequency'], data['nr_band'], data['rsrp'],
                data['nr_pci'], data['rsrq'], data['latitude'], data['longitude'],
                data['location_description'], data['timestamp'], data['photo_path']
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error inserting signal data: {e}")
            return False
    
    def get_signal_data(self, limit=100, offset=0):
        """Get signal data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM signal_data 
                ORDER BY timestamp DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            rows = cursor.fetchall()
            conn.close()
            
            # Convert rows to dicts
            from models.signal_data import SignalData
            signal_data_list = []
            
            for row in rows:
                data_dict = dict(row)
                signal_data = SignalData.from_dict(data_dict)
                signal_data_list.append(signal_data)
            
            return signal_data_list
        except Exception as e:
            print(f"Error getting signal data: {e}")
            return []
    
    def get_signal_data_count(self):
        """Get total count of signal data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM signal_data')
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
        except Exception as e:
            print(f"Error getting signal data count: {e}")
            return 0
    
    def export_to_csv(self, file_path=None):
        """Export data to CSV"""
        try:
            if not file_path:
                # Generate default file path
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_path = f'signal_data_{timestamp}.csv'
            
            # Get all data
            signal_data_list = self.get_signal_data(limit=10000)
            
            if not signal_data_list:
                print("No data to export")
                return None
            
            # Convert to DataFrame
            data_list = [data.to_dict() for data in signal_data_list]
            df = pd.DataFrame(data_list)
            
            # Export to CSV
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"Data exported to: {file_path}")
            return file_path
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None
    
    def export_to_excel(self, file_path=None):
        """Export data to Excel"""
        try:
            if not file_path:
                # Generate default file path
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_path = f'signal_data_{timestamp}.xlsx'
            
            # Get all data
            signal_data_list = self.get_signal_data(limit=10000)
            
            if not signal_data_list:
                print("No data to export")
                return None
            
            # Convert to DataFrame
            data_list = [data.to_dict() for data in signal_data_list]
            df = pd.DataFrame(data_list)
            
            # Export to Excel
            df.to_excel(file_path, index=False)
            print(f"Data exported to: {file_path}")
            return file_path
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return None
    
    def delete_all_data(self):
        """Delete all signal data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM signal_data')
            conn.commit()
            conn.close()
            print("All data deleted")
            return True
        except Exception as e:
            print(f"Error deleting all data: {e}")
            return False
