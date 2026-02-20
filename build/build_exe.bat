@echo off
setlocal

python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

pyinstaller --noconfirm --clean bkp6.spec
if errorlevel 1 exit /b 1

echo Build complete: dist\bkp6-mvp.exe
