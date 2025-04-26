"""
Setup script to properly configure the environment for face recognition.
"""
import sys
import os
import subprocess
import platform

def main():
    print("Setting up the face recognition environment...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major == 3 and python_version.minor >= 12:
        print("⚠️ Warning: Python 3.12+ may have compatibility issues with some CV libraries.")
        print("Consider using Python 3.9 or 3.10 for best compatibility.")
    
    # Install dependencies in the correct order
    dependencies = [
        "numpy==1.24.3",  # Install specific numpy version first
        "dlib>=19.7.0",   # Install dlib before face_recognition
        "-r requirements.txt"  # Then install everything else
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        except subprocess.CalledProcessError:
            print(f"Failed to install {dep}")
            if "dlib" in dep:
                print("Note: dlib installation may require C++ build tools.")
                if platform.system() == "Windows":
                    print("On Windows, install Visual Studio with C++ build tools.")
                elif platform.system() == "Linux":
                    print("On Linux, install build-essential and cmake.")
                elif platform.system() == "Darwin":  # macOS
                    print("On macOS, install Xcode command line tools.")
    
    print("\nSetup complete. Verifying installations:")
    try:
        import compat
        compat.ensure_environment()
    except ImportError:
        print("Please run this script again to resolve any remaining issues.")

if __name__ == "__main__":
    main()
