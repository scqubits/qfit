#!/bin/bash

# Step 0: Run the terminal command to convert the UI file to Python code
pyside6-rcc -o resources_rc.py resources.qrc

# Step 1: Run the terminal command to convert the UI file to Python code
pyside6-uic ui_window.ui -o ui_window.py
pyside6-uic ui_menu.ui -o ui_menu.py
pyside6-uic settings.ui -o settings.py

# Step 2: Change the all of the wrong import of ui_window.py
sed -i '' 's/import resources_rc/from . import resources_rc/g' ui_window.py
sed -i '' 's/import resources_rc/from . import resources_rc/g' settings.py

# Step 3: Move the ui_window.py to the folder ./../ui_designer/
mv ui_window.py ./../qfit/ui_designer/
mv resources_rc.py ./../qfit/ui_designer/
mv ui_menu.py ./../qfit/ui_designer/
mv settings.py ./../qfit/ui_designer/

echo "All tasks completed."
