import sys
import subprocess
import pkg_resources

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Check installed packages
print("\nInstalled packages:")
for pkg in ['numpy', 'pandas', 'face_recognition', 'dlib', 'cv2', 'streamlit']:
    try:
        version = pkg_resources.get_distribution(pkg if pkg != 'cv2' else 'opencv-python').version
        print(f"✓ {pkg}: {version}")
    except pkg_resources.DistributionNotFound:
        print(f"✗ {pkg}: Not installed")
    except Exception as e:
        print(f"? {pkg}: Error checking version - {str(e)}")
