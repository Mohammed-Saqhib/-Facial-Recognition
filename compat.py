"""
Compatibility module for face recognition system.
This module helps manage package dependencies and ensures version compatibility.
"""
import sys
import os
import importlib
from importlib.metadata import version, PackageNotFoundError
import subprocess
import pkg_resources

def check_dependencies():
    """Check if all required dependencies are installed with compatible versions."""
    required_packages = {
        'numpy': '<=2.0.0',  # OpenCV works better with numpy 1.x
        'opencv-python': '==4.5.5.64',
        'face_recognition': '==1.3.0',
        'dlib': '>=19.7.0'
    }
    
    missing_or_incompatible = []
    
    for package, version_constraint in required_packages.items():
        try:
            pkg_resources.require(f"{package}{version_constraint}")
        except (pkg_resources.VersionConflict, pkg_resources.DistributionNotFound):
            missing_or_incompatible.append(package)
    
    return missing_or_incompatible

def fix_numpy_opencv_compatibility():
    """
    Try to fix numpy/OpenCV compatibility issues by downgrading numpy if needed.
    Returns True if action was taken, False otherwise.
    """
    try:
        import numpy
        np_version = numpy.__version__
        if np_version.startswith('2.'):
            print("Detected numpy 2.x which may be incompatible with OpenCV 4.5.5")
            print("Attempting to install a compatible numpy version...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy==1.24.3', '--force-reinstall'])
            return True
    except Exception as e:
        print(f"Error checking numpy version: {e}")
        return False
    
    return False

def ensure_environment():
    """
    Ensure the environment is properly set up for face recognition.
    """
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"Missing or incompatible packages: {', '.join(missing_packages)}")
        print("Attempting to fix environment...")
        
        # If numpy is in the list, try to fix numpy/OpenCV compatibility
        if 'numpy' in missing_packages:
            fixed = fix_numpy_opencv_compatibility()
            if fixed:
                print("Numpy version has been adjusted. Please restart your application.")
                return False
    
    try:
        # Test imports
        import cv2
        import face_recognition
        print("Environment check passed. All required packages are available.")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please fix package dependencies before running the application.")
        return False

if __name__ == "__main__":
    # When run directly, perform environment check
    if ensure_environment():
        print("All dependencies are properly installed.")
    else:
        print("Please restart the application after fixing dependencies.")
