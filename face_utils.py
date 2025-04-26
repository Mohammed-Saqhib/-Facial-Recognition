import face_recognition
import numpy as np
import cv2

class FaceDetector:
    def __init__(self):
        pass
        
    def detect_faces(self, frame):
        # Convert BGR to RGB (face_recognition uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Use face_recognition to find face locations
        face_locations = face_recognition.face_locations(rgb_frame)
        return face_locations

class FaceRecognizer:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []

    def compute_face_encoding(self, frame, face_location):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            return face_recognition.face_encodings(rgb_frame, [face_location])[0]
        except:
            return None

    def add_face(self, face_encoding, name, face_id):
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(name)
        self.known_face_ids.append(face_id)

    def recognize_face(self, face_encoding):
        if len(self.known_face_encodings) == 0:
            return None

        # Compare face with known faces
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        # If the closest match is within tolerance, return the name and ID
        if face_distances[best_match_index] < 0.6:  # Tolerance threshold
            return {
                'name': self.known_face_names[best_match_index],
                'id': self.known_face_ids[best_match_index],
                'confidence': 1 - face_distances[best_match_index]
            }
        return None

    def load_known_faces(self, encodings, names, ids):
        self.known_face_encodings = encodings
        self.known_face_names = names
        self.known_face_ids = ids
