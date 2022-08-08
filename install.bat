@echo off
curl --ssl-no-revoke -SL https://www.7-zip.org/a/7zr.exe -O
curl --ssl-no-revoke -SL https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z -O
7zr.exe x ffmpeg-git-full.7z
setx path "%PATH%;%CD%\ffmpeg-2022-08-03-git-d3f48e68b3-full_build\bin"
