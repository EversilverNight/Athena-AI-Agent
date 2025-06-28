@echo off
title Athena Setup
cd /d %~dp0
echo Installing Python dependencies...
pip install -r requirements.txt
echo Done! Athena is ready to launch.
pause
