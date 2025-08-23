@echo off
echo ========================================
echo Tradelink Intercom System - Installer
echo ========================================
echo.

echo Copying executable to Program Files...
if not exist "C:\Program Files\TradelinkIntercom" mkdir "C:\Program Files\TradelinkIntercom"

copy "dist\TradelinkIntercom.exe" "C:\Program Files\TradelinkIntercom\"

echo.
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Tradelink Intercom.lnk'); $Shortcut.TargetPath = 'C:\Program Files\TradelinkIntercom\TradelinkIntercom.exe'; $Shortcut.Save()"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo The Tradelink Intercom System has been installed to:
echo C:\Program Files\TradelinkIntercom\
echo.
echo A desktop shortcut has been created.
echo.
echo To run the system, double-click the desktop shortcut.
echo.
pause
