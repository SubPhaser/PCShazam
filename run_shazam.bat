@echo off
echo Running Shazam script...
:: Change to the directory of the batch file
cd /d "%~dp0"
:: Run the Python script
python "shazam.py"
echo.
echo Script finished. Closing in 5 seconds...
:: Wait for 5 seconds and then close
timeout /t 5 /nobreak >nul