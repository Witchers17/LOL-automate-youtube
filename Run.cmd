@echo off
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
git restore .> log.txt 2>&1
git pull> log.txt 2>&1
@echo off
pip install -r requirements.txt > log.txt 2>&1

call python video_maker/main.py


