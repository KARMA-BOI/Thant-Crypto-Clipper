@echo off

pip install pyinstaller

pyinstaller --onefile --hidden-import=early "DO NOT RUN.py" -i 1.ico


