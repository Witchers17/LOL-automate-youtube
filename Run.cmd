@echo off
echo Activating virtual environment...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
echo Updating from remote repository...
git restore .
git pull
echo Installing dependencies...
pip install -r requirements.txt
echo Running script...
call python video_maker/main.py


