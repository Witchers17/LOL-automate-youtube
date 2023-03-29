@echo off
echo Activating virtual environment...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
echo Updating from remote repository...
@REM git restore .
git pull
echo Installing dependencies...
@echo off
pip install -r requirements.txt
echo Running script...
call python video_maker/main.py


