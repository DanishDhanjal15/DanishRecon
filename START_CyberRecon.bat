@echo off
:: CyberRecon-Pro Launcher
:: This ensures all tools are in PATH before starting

echo Starting CyberRecon-Pro...
echo.

:: Twilio WhatsApp login alert configuration.
:: IMPORTANT: Use your Twilio account values. Do not commit real secrets to this file.
:: For new accounts, the WhatsApp Sandbox sender is usually whatsapp:+14155238886.
if not defined DANISHRECON_TWILIO_ACCOUNT_SID set "DANISHRECON_TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
if not defined DANISHRECON_TWILIO_AUTH_TOKEN set "DANISHRECON_TWILIO_AUTH_TOKEN=CHANGE_ME"
if not defined DANISHRECON_TWILIO_WHATSAPP_FROM set "DANISHRECON_TWILIO_WHATSAPP_FROM=whatsapp:+14155238886"
if not defined DANISHRECON_TWILIO_WHATSAPP_TO set "DANISHRECON_TWILIO_WHATSAPP_TO=whatsapp:+RECIPIENT1;whatsapp:+RECIPIENT2"

if /I "%DANISHRECON_TWILIO_AUTH_TOKEN%"=="CHANGE_ME" (
	set "DANISHRECON_TWILIO_ENABLED=0"
	echo Twilio WhatsApp alert is disabled. Set DANISHRECON_TWILIO_ACCOUNT_SID and DANISHRECON_TWILIO_AUTH_TOKEN to enable it.
) else (
	set "DANISHRECON_TWILIO_ENABLED=1"
	echo Twilio WhatsApp alert is enabled for this launch.
	echo If you see Twilio code 63007, your sender is not WhatsApp-enabled for this account.
	echo Use the sender shown in Twilio Console ^> Messaging ^> Try it out ^> Send a WhatsApp message.
)
echo.

:: Set GOPATH
set GOPATH=%USERPROFILE%\go

:: Add all tools to PATH for this session
set PATH=%PATH%;C:\Program Files\Go\bin
set PATH=%PATH%;%GOPATH%\bin
set PATH=%PATH%;%USERPROFILE%\Downloads\strawberry-perl-5.42.0.1-64bit-PDL\perl\bin
set PATH=%PATH%;%USERPROFILE%\Downloads\strawberry-perl-5.42.0.1-64bit-PDL\c\bin
set PATH=%PATH%;c:\Users\Danish\OneDrive\Desktop\recon cyber\nikto\program
set PATH=%PATH%;c:\Users\Danish\OneDrive\Desktop\recon cyber\exploit-database

:: Navigate to CyberRecon-Pro directory
cd /d "C:\Users\Danish\OneDrive\Desktop\recon cyber\CyberRecon-Pro"

:: Launch with virtual environment Python
"C:\Users\Danish\OneDrive\Desktop\recon cyber\.venv\Scripts\python.exe" Cyber_recon_pro.py

pause
