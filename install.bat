@echo off
curl --ssl-no-revoke -SL https://www.7-zip.org/a/7zr.exe -O
curl --ssl-no-revoke -SL https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z -O
7zr.exe x ffmpeg-git-full.7z
pip install -r requirements.txt
playwright install chrome
(echo @echo off & echo python %~dp0\main.py %*) > pydl.bat
