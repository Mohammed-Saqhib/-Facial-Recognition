"""
This script patches the face_recognition module to use our custom models provider
instead of the original face_recognition_models package.
"""
import sys
import importlib

try:
    # First try to import the original module
    import face_recognition_models
    print("Successfully imported face_recognition_models")
except ImportError:
    # If that fails, use our patched version
    print("Using patched face_recognition_models")
    import patched_face_recognition_models
    sys.modules['face_recognition_models'] = patched_face_recognition_models
    
    # Reload face_recognition to make sure it uses our patched module
    if 'face_recognition.api' in sys.modules:
        importlib.reload(sys.modules['face_recognition.api'])
    if 'face_recognition' in sys.modules:
        importlib.reload(sys.modules['face_recognition'])

# Now face_recognition should work
import face_recognition
print("face_recognition module is ready to use")
