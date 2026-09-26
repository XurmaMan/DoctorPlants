@echo off
python -m pip install -r requirements.txt
python app.py
if errorlevel 1 py app.py
pause
