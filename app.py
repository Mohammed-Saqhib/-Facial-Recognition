import os
import sys

# Apply the patch
try:
    import face_recognition_patch
except ImportError as e:
    print(f"Error importing patch: {e}")

import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
from face_utils import FaceDetector, FaceRecognizer
from database import Database

# Set page config
st.set_page_config(
    page_title="Face Attendance System",
    page_icon="👤",
    layout="wide"
)

# Initialize session state
if 'registration_mode' not in st.session_state:
    st.session_state.registration_mode = False
if 'recognized_person' not in st.session_state:
    st.session_state.recognized_person = None
if 'last_attendance' not in st.session_state:
    st.session_state.last_attendance = None

# Initialize resources
@st.cache_resource
def load_resources():
    face_detector = FaceDetector()
    face_recognizer = FaceRecognizer()
    db = Database()
    
    # Load known faces from database
    encodings, names, ids = db.load_faces()
    if encodings:
        face_recognizer.load_known_faces(encodings, names, ids)
    
    return face_detector, face_recognizer, db

face_detector, face_recognizer, db = load_resources()

# Functions
def toggle_registration():
    if st.session_state.registration_mode:
        st.session_state.registration_mode = False
    else:
        if not reg_name or not reg_id:
            st.sidebar.error("Name and ID are required for registration")
        else:
            st.session_state.registration_mode = True

def process_image(image):
    if image is None:
        return None
    
    # Convert the image to numpy array
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    # Detect faces
    face_locations = face_detector.detect_faces(opencv_image)
    
    if not face_locations:
        return "No face detected", None
    
    # Draw rectangles around faces
    img_with_faces = opencv_image.copy()
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(img_with_faces, (left, top), (right, bottom), (0, 255, 0), 2)
    
    # Registration mode
    if st.session_state.registration_mode:
        face_location = face_locations[0]  # Use the first detected face
        face_encoding = face_recognizer.compute_face_encoding(opencv_image, face_location)
        
        if face_encoding is not None:
            # Add face to recognizer
            face_recognizer.add_face(face_encoding, reg_name, reg_id)
            
            # Save to database
            db.save_faces(
                face_recognizer.known_face_encodings,
                face_recognizer.known_face_names,
                face_recognizer.known_face_ids
            )
            
            st.session_state.registration_mode = False
            return f"Successfully registered {reg_name} (ID: {reg_id})", cv2.cvtColor(img_with_faces, cv2.COLOR_BGR2RGB)
        else:
            return "Failed to compute face encoding", cv2.cvtColor(img_with_faces, cv2.COLOR_BGR2RGB)
    
    # Recognition mode
    else:
        recognition_results = []
        
        for face_location in face_locations:
            face_encoding = face_recognizer.compute_face_encoding(opencv_image, face_location)
            if face_encoding is not None:
                person = face_recognizer.recognize_face(face_encoding)
                
                if person:
                    # Mark attendance
                    attendance_marked = db.mark_attendance(person['id'], person['name'])
                    attendance_status = "Attendance marked!" if attendance_marked else "Already marked today"
                    
                    recognition_results.append({
                        'name': person['name'],
                        'id': person['id'],
                        'confidence': person['confidence'],
                        'attendance_status': attendance_status
                    })
        
        if recognition_results:
            return recognition_results, cv2.cvtColor(img_with_faces, cv2.COLOR_BGR2RGB)
        else:
            return "No known faces detected", cv2.cvtColor(img_with_faces, cv2.COLOR_BGR2RGB)

# UI Layout
st.title("Face Attendance System")

# Sidebar
st.sidebar.title("Controls")

# Registration section
st.sidebar.header("Registration")
reg_name = st.sidebar.text_input("Name", key="reg_name")
reg_id = st.sidebar.text_input("ID", key="reg_id")

register_button = st.sidebar.button(
    "Start Registration" if not st.session_state.registration_mode else "Cancel Registration", 
    on_click=toggle_registration
)

# Status and mode display
status = "👥 Registration Mode" if st.session_state.registration_mode else "🔍 Recognition Mode"
st.sidebar.markdown(f"**Current Mode:** {status}")

# Attendance records section
st.sidebar.header("View Records")
selected_date = st.sidebar.date_input("Select Date", datetime.now())

# Main content - Two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Camera Input")
    camera_image = st.camera_input("Capture", key="camera")

    # Show information about current mode
    if st.session_state.registration_mode:
        st.info("Position your face in the camera and take a picture to register")
    else:
        st.info("Take a picture to mark attendance")

with col2:
    st.subheader("Results")
    result_placeholder = st.empty()
    image_placeholder = st.empty()

# Process the captured image
if camera_image:
    result, processed_image = process_image(camera_image)
    
    if processed_image is not None:
        image_placeholder.image(processed_image)
    
    if result == "No face detected":
        result_placeholder.warning(result)
    elif isinstance(result, str):
        result_placeholder.success(result)
    elif isinstance(result, list):
        for i, person in enumerate(result):
            result_placeholder.success(
                f"**Recognized:** {person['name']} (ID: {person['id']})\n\n"
                f"Confidence: {person['confidence']:.2f}\n\n"
                f"{person['attendance_status']}"
            )

# Display attendance records
st.header("Attendance Records")
selected_date_str = selected_date.strftime("%Y-%m-%d")
records = db.get_attendance_records(selected_date_str)

if not records.empty:
    # Format time for display
    records['Time'] = pd.to_datetime(records['timestamp']).dt.strftime('%I:%M %p')
    display_df = records[['id', 'name', 'Time']]
    st.dataframe(display_df, use_container_width=True)
else:
    st.info(f"No attendance records for {selected_date_str}")

# Instructions
st.sidebar.markdown("---")
st.sidebar.markdown("### How to use")
st.sidebar.markdown(""" 
1. **Recognition Mode**: Just take a picture to mark attendance 
2. **Registration Mode**: Enter a name and ID, click 'Start Registration', then take a picture 
""")
