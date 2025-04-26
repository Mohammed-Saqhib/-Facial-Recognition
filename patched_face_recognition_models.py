"""
This is a patched version of face_recognition_models that doesn't rely on pkg_resources.
Instead, it uses direct file paths to the installed models.
"""

import os

# Find the installed location
import site
site_packages = site.getsitepackages()
for site_path in site_packages:
    model_path = os.path.join(site_path, 'face_recognition_models', 'models')
    if os.path.exists(model_path):
        MODELS_PATH = model_path
        break
else:
    # If not found in site-packages, try the current directory's environment
    current_dir = os.path.dirname(os.path.abspath(__file__))
    face_env_path = os.path.join(current_dir, 'face_env', 'Lib', 'site-packages', 'face_recognition_models', 'models')
    if os.path.exists(face_env_path):
        MODELS_PATH = face_env_path
    else:
        raise ImportError("Cannot find face_recognition_models installation path")

def pose_predictor_model_location():
    """Returns the path to the pose predictor model."""
    return os.path.join(MODELS_PATH, "shape_predictor_68_face_landmarks.dat")

def pose_predictor_five_point_model_location():
    """Returns the path to the 5-point pose predictor model."""
    return os.path.join(MODELS_PATH, "shape_predictor_5_face_landmarks.dat")

def face_recognition_model_location():
    """Returns the path to the face recognition model."""
    return os.path.join(MODELS_PATH, "dlib_face_recognition_resnet_model_v1.dat")

def cnn_face_detector_model_location():
    """Returns the path to the face detection model."""
    return os.path.join(MODELS_PATH, "mmod_human_face_detector.dat")
