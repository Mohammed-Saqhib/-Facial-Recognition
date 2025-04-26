import os
import pandas as pd
from datetime import datetime

class AttendanceTracker:
    def __init__(self, database):
        self.db = database
    
    def mark_attendance(self, person_id):
        """Mark attendance for a person"""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Get today's date
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Check if the person has already been marked present today
        today_attendance = self.db.get_attendance_by_date(today)
        if person_id in today_attendance:
            # Already marked attendance
            return False
        
        # Record attendance
        return self.db.record_attendance(person_id, current_time)
    
    def get_today_attendance(self):
        """Get today's attendance records"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.db.get_attendance_by_date(today)
    
    def export_to_csv(self, date=None):
        """Export attendance records to CSV file"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        attendance_data = self.db.get_attendance_by_date(date)
        
        data = []
        for person_id, record in attendance_data.items():
            data.append({
                "ID": person_id,
                "Name": record["name"],
                "Time": record["time"],
                "Date": date
            })
        
        # Create DataFrame
        if data:
            df = pd.DataFrame(data)
            
            # Create export directory if it doesn't exist
            export_dir = "data/attendance_logs/exports"
            os.makedirs(export_dir, exist_ok=True)
            
            # Save to CSV
            filename = f"{export_dir}/attendance_{date}.csv"
            df.to_csv(filename, index=False)
            return filename
        else:
            return None
