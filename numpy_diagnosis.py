import sys
import os

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Check numpy installation
try:
    import numpy
    print(f"NumPy version: {numpy.__version__}")
    print(f"NumPy path: {numpy.__path__}")
    
    # Try importing problematic modules
    print("\nTesting critical imports:")
    from numpy._core import multiarray
    print("✓ numpy._core.multiarray imported successfully")
    from numpy.core import multiarray
    print("✓ numpy.core.multiarray imported successfully")
    from numpy._core import _multiarray_umath
    print("✓ numpy._core._multiarray_umath imported successfully")
    
    print("\nNumPy seems to be working correctly.")
    
except ImportError as e:
    print(f"\nImportError detected: {e}")
    print("\nNumPy installation appears to be corrupted or incompatible.")
except Exception as e:
    print(f"\nUnexpected error: {e}")
