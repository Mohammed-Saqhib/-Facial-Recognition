import cv2
import face_recognition

class FaceDetector:
    def __init__(self):
        # The HOG method is faster but less accurate, CNN is more accurate but slower
        self.detection_method = "hog"  # Options: "hog", "cnn"
    
    def detect_faces(self, frame):
        """
        Detect faces in the given frame
        
        Args:
            frame: The image frame to process
            
        Returns:
            List of face locations in (top, right, bottom, left) format
        """
        # Resize frame for faster processing (optional)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convert from BGR to RGB (face_recognition uses RGB)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find all face locations
        face_locations = face_recognition.face_locations(rgb_small_frame, model=self.detection_method)
        
        # Scale back the face locations
        face_locations = [(top * 4, right * 4, bottom * 4, left * 4) 
                         for top, right, bottom, left in face_locations]
        
        return face_locations
