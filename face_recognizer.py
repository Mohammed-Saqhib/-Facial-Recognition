import face_recognition
import numpy as np
import cv2

class FaceRecognizer:
    def __init__(self, database):
        self.db = database
        self.tolerance = 0.6  # Lower is more strict
    
    def compute_face_encoding(self, frame, face_location):
        """
        Compute the encoding for a detected face
        
        Args:
            frame: The image frame
            face_location: (top, right, bottom, left) tuple of the face
            
        Returns:
            face_encoding: The 128-dimensional encoding of the face
        """
        top, right, bottom, left = face_location
        face_image = frame[top:bottom, left:right]
        
        # Convert from BGR to RGB
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        
        # Get face encoding
        face_encodings = face_recognition.face_encodings(face_image)
        
        if len(face_encodings) > 0:
            return face_encodings[0]
        else:
            return None
    
    def identify_face(self, face_encoding):
        """
        Identify a face from known faces in the database
        
        Args:
            face_encoding: The encoding of the face to identify
            
        Returns:
            (name, id, confidence): Tuple with identity info or (None, None, 0) if not recognized
        """
        known_faces = self.db.get_all_face_encodings()
        
        if not known_faces:
            return None, None, 0
        
        # Compare face with known faces
        face_encodings = [np.array(encoding) for _, _, encoding in known_faces]
        face_ids = [id for id, _, _ in known_faces]
        face_names = [name for _, name, _ in known_faces]
        
        matches = face_recognition.compare_faces(face_encodings, face_encoding, self.tolerance)
        
        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(face_encodings, face_encoding)
        
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            confidence = 1 - face_distances[best_match_index]
            
            if matches[best_match_index]:
                return face_names[best_match_index], face_ids[best_match_index], confidence
        
        return None, None, 0
