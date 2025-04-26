import sys
import subprocess
import os

def run_command(command):
    print(f"Running: {' '.join(command)}")
    process = subprocess.run(command, capture_output=True, text=True)
    
    if process.returncode != 0:
        print("Error occurred:")
        print(process.stderr)
        return False
    
    print("Output:")
    print(process.stdout)
    return True

# Get pip path from the current Python environment
pip_path = os.path.join(os.path.dirname(sys.executable), 'pip')
if sys.platform == 'win32':
    pip_path += '.exe'

print(f"Using pip: {pip_path}")

# First uninstall pandas to avoid conflicts
print("\nStep 1: Uninstalling pandas...")
run_command([pip_path, 'uninstall', '-y', 'pandas'])

# Then uninstall numpy
print("\nStep 2: Uninstalling numpy...")
run_command([pip_path, 'uninstall', '-y', 'numpy'])

# Install numpy first - with specific version known to work well
print("\nStep 3: Installing NumPy 1.23.5 (compatible version)...")
run_command([pip_path, 'install', 'numpy==1.23.5'])

# Install pandas next
print("\nStep 4: Installing pandas...")
run_command([pip_path, 'install', 'pandas'])

# Verify face_recognition dependencies
print("\nStep 5: Installing face_recognition dependencies if needed...")
run_command([pip_path, 'install', '--no-deps', '--force-reinstall', 'dlib'])
run_command([pip_path, 'install', '--no-deps', '--force-reinstall', 'face_recognition'])

print("\nDone! Try running your application again.")
