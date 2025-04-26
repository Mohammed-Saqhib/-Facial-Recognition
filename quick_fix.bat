@echo off
echo Fixing NumPy and Pandas compatibility...

echo 1. Activating environment...
call face_env\Scripts\activate.bat

echo 2. Uninstalling pandas...
pip uninstall -y pandas

echo 3. Uninstalling numpy...
pip uninstall -y numpy
pip uninstall -y numpy  

echo 4. Installing compatible NumPy version...
pip install numpy==1.23.5

echo 5. Reinstalling pandas...
pip install pandas

echo 6. Reinstalling other dependencies if needed...
pip install --no-deps --force-reinstall dlib
pip install --no-deps --force-reinstall face_recognition
pip install --no-deps --force-reinstall opencv-python

echo Done! Try running your application again.
pause
