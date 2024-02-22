#!/bin/bash

# Step 0: Run the terminal command to convert the UI file to Python code
pyside6-rcc -o resources_rc.py resources.qrc

# Step 1: Run the terminal command to convert the UI file to Python code
pyside6-uic ui_window.ui -o ui_window.py
pyside6-uic ui_menu.ui -o ui_menu.py
pyside6-uic settings_fit.ui -o settings_fit.py
pyside6-uic settings_visual.ui -o settings_visual.py
pyside6-uic settings_numerical_spectrum.ui -o settings_numerical_spectrum.py

# Step 2: Change line 29 of ui_window.py
sed -i '' '29s/import resources_rc/from . import resources_rc/' ui_window.py
sed -i '' '22s/import resources_rc/from . import resources_rc/' settings_fit.py
sed -i '' '23s/import resources_rc/from . import resources_rc/' settings_numerical_spectrum.py
sed -i '' '21s/import resources_rc/from . import resources_rc/' settings_visual.py

# Step 3: Move the ui_window.py to the folder ./../ui_designer/
mv ui_window.py ./../qfit/ui_designer/
mv resources_rc.py ./../qfit/ui_designer/
mv ui_menu.py ./../qfit/ui_designer/
mv settings_fit.py ./../qfit/ui_designer/
mv settings_visual.py ./../qfit/ui_designer/
mv settings_numerical_spectrum.py ./../qfit/ui_designer/

echo "All tasks completed."
