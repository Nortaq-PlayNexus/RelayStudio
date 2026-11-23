@echo off
setlocal
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Relay Studio needs Node.js 20 or later.
  echo Install it from the official Node.js website, then run this file again.
  pause
  exit /b 1
)
set HOST=127.0.0.1
set PORT=3000
title Relay Studio - local preview server
echo Starting Relay Studio at http://127.0.0.1:3000
echo Keep this window open. Press Ctrl+C to stop the server.
echo This launcher opens a browser prototype, not an installed native application.
start "" powershell.exe -NoProfile -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:3000'"
node server.mjs
if errorlevel 1 pause
endlocal
