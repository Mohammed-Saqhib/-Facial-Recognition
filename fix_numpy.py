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

# First try to uninstall numpy
print("\nStep 1: Uninstalling NumPy...")
run_command([pip_path, 'uninstall', '-y', 'numpy'])

# Make sure it's completely removed
print("\nStep 2: Making sure NumPy is completely removed...")
run_command([pip_path, 'uninstall', '-y', 'numpy'])

# Install numpy fresh
print("\nStep 3: Installing NumPy again...")
run_command([pip_path, 'install', 'numpy==1.24.3'])  # Using a stable version

# Install opencv-python again (if needed)
print("\nStep 4: Reinstalling OpenCV...")
run_command([pip_path, 'uninstall', '-y', 'opencv-python'])
run_command([pip_path, 'install', 'opencv-python'])

print("\nDone! Try running your application again.")
