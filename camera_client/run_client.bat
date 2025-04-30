@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Running camera client...
python client.py

pause