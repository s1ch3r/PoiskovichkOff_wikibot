@echo off
call %~dp0telegram_bot\venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN=5289504159:AAGcpkOnGOE9MoNLu-9PW_G2UhYJPiiqgnI

python bot_telegram.py

pause