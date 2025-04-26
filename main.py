import compat

# Check environment before proceeding
if not compat.ensure_environment():
    print("Environment issues detected. Please fix dependencies and restart.")
    import sys
    sys.exit(1)

# Now proceed with regular imports
import cv2
import numpy as np
import os
from face_detector import FaceDetector
from face_recognizer import FaceRecognizer
from attendance import AttendanceTracker
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
from database import Database

class FaceAttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Attendance System")
        self.root.geometry("800x600")
        
        # Initialize components
        self.setup_directories()
        self.db = Database()
        self.face_detector = FaceDetector()
        self.face_recognizer = FaceRecognizer(self.db)
        self.attendance_tracker = AttendanceTracker(self.db)
        
        self.camera_active = False
        self.registration_mode = False
        self.current_name = tk.StringVar()
        self.current_id = tk.StringVar()
        
        self.setup_ui()
    
    def setup_directories(self):
        dirs = [
            'data',
            'data/faces',
            'data/attendance_logs'
        ]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    def setup_ui(self):
        # Frame for video feed
        self.video_frame = tk.Frame(self.root, width=640, height=480)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.video_label = tk.Label(self.video_frame)
        self.video_label.grid(row=0, column=0)
        
        # Control panel
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=1, column=0, padx=10, pady=10)
        
        # Registration controls
        reg_frame = tk.LabelFrame(control_frame, text="Registration")
        reg_frame.grid(row=0, column=0, padx=10, pady=10)
        
        tk.Label(reg_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(reg_frame, textvariable=self.current_name).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(reg_frame, text="ID:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(reg_frame, textvariable=self.current_id).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(reg_frame, text="Register Face", command=self.toggle_registration).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # Attendance controls
        att_frame = tk.LabelFrame(control_frame, text="Attendance")
        att_frame.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Button(att_frame, text="Start Attendance", command=self.toggle_camera).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(att_frame, text="Export Records", command=self.export_attendance).grid(row=1, column=0, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("System Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, sticky=tk.W+tk.E)
    
    def toggle_camera(self):
        if not self.camera_active:
            self.camera_active = True
            self.video_thread = threading.Thread(target=self.update_frame)
            self.video_thread.daemon = True
            self.video_thread.start()
            self.status_var.set("Camera Active - Attendance Mode")
        else:
            self.camera_active = False
            self.status_var.set("Camera Stopped")
    
    def toggle_registration(self):
        if not self.current_name.get() or not self.current_id.get():
            messagebox.showerror("Error", "Name and ID are required for registration")
            return
            
        self.registration_mode = not self.registration_mode
        if self.registration_mode:
            self.toggle_camera()
            self.status_var.set("Registration Mode - Capturing Face")
        else:
            self.registration_mode = False
    
    def update_frame(self):
        cap = cv2.VideoCapture(0)
        
        while self.camera_active:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Face processing
            face_locations = self.face_detector.detect_faces(frame)
            
            if self.registration_mode and face_locations:
                # Register the first detected face
                face_encoding = self.face_recognizer.compute_face_encoding(frame, face_locations[0])
                if face_encoding is not None:
                    name = self.current_name.get()
                    id = self.current_id.get()
                    self.db.add_person(id, name, face_encoding)
                    self.status_var.set(f"Registered: {name} ({id})")
                    self.registration_mode = False
            
            elif face_locations:
                # Attendance mode
                for face_location in face_locations:
                    face_encoding = self.face_recognizer.compute_face_encoding(frame, face_location)
                    if face_encoding is not None:
                        name, id, confidence = self.face_recognizer.identify_face(face_encoding)
                        if name and confidence > 0.6:  # Adjust threshold as needed
                            self.attendance_tracker.mark_attendance(id)
                            self.status_var.set(f"Attendance marked for: {name}")
                            # Draw rectangle around face
                            top, right, bottom, left = face_location
                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Display the frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            
        cap.release()
    
    def export_attendance(self):
        filename = self.attendance_tracker.export_to_csv()
        messagebox.showinfo("Export Complete", f"Attendance exported to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceAttendanceSystem(root)
    root.mainloop()
