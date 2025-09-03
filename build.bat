@echo off
echo ===============================
echo Building Whiteboard App (.exe) 
echo ===============================

REM Delete old build and dist folders
rmdir /s /q build
rmdir /s /q dist

REM Run PyInstaller with all image assets
pyinstaller --onefile --windowed ^
  --icon=assets\logo1.ico ^
  --add-data "assets;assets" ^
  main.py

echo.
echo ===============================
echo Creating Installer (setup.exe)
echo ===============================

REM Path to Inno Setup Compiler (edit if installed elsewhere)
set INNO_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

%INNO_PATH% installer.iss

echo.
echo ===============================
echo Build complete! setup.exe ready.
echo ===============================
pause
