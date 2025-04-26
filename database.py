import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.faces_file = os.path.join(data_dir, "faces.json")
        self.attendance_file = os.path.join(data_dir, "attendance.csv")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        if not os.path.exists(self.faces_file):
            self.save_faces([], [], [])
        
        if not os.path.exists(self.attendance_file):
            df = pd.DataFrame(columns=['id', 'name', 'timestamp'])
            df.to_csv(self.attendance_file, index=False)

    def save_faces(self, encodings, names, ids):
        # Convert numpy arrays to lists for JSON serialization
        serializable_encodings = [enc.tolist() if isinstance(enc, np.ndarray) else enc for enc in encodings]
        
        data = {
            'encodings': serializable_encodings,
            'names': names,
            'ids': ids
        }
        
        with open(self.faces_file, 'w') as f:
            json.dump(data, f)

    def load_faces(self):
        if not os.path.exists(self.faces_file):
            return [], [], []
        
        with open(self.faces_file, 'r') as f:
            data = json.load(f)
        
        # Convert lists back to numpy arrays
        encodings = [np.array(enc) if enc else None for enc in data['encodings']]
        names = data['names']
        ids = data['ids']
        
        return encodings, names, ids

    def mark_attendance(self, person_id, name):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Read existing attendance
        df = pd.read_csv(self.attendance_file)
        
        # Check if this person has already been marked today
        today = now.strftime("%Y-%m-%d")
        today_records = df[pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d') == today]
        
        if person_id in today_records['id'].values:
            return False  # Already marked attendance today
        
        # Add new attendance record
        new_record = pd.DataFrame({'id': [person_id], 'name': [name], 'timestamp': [timestamp]})
        df = pd.concat([df, new_record], ignore_index=True)
        
        # Save back to file
        df.to_csv(self.attendance_file, index=False)
        return True

    def get_attendance_records(self, date=None):
        if not os.path.exists(self.attendance_file):
            return pd.DataFrame(columns=['id', 'name', 'timestamp'])
        
        df = pd.read_csv(self.attendance_file)
        
        if date:
            # Filter records for a specific date
            df['date'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')
            df = df[df['date'] == date]
            df = df.drop(columns=['date'])
        
        return df
