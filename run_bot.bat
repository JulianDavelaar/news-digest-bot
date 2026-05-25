@echo off
cd /d "C:\projects\news-digest-bot"
set PYTHONIOENCODING=utf-8
python news.py >> log.txt 2>&1