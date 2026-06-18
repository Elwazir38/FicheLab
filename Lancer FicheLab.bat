@echo off
chcp 65001 >nul
title FicheLab
cd /d "%~dp0"

echo ============================================
echo            Demarrage de FicheLab
echo ============================================
echo.

REM --- Verification du venv ---
if not exist ".venv\Scripts\python.exe" (
  echo [ERREUR] Environnement Python introuvable ^(.venv^).
  echo Ouvrez PowerShell dans ce dossier et lancez :
  echo     python -m venv .venv
  echo     .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  echo     .\.venv\Scripts\python.exe -m pip install -e engines\pyromaths
  echo.
  pause
  exit /b 1
)

REM --- Ouvre le navigateur dans 3 secondes, sans bloquer le serveur ---
start "" /min powershell -WindowStyle Hidden -Command "Start-Sleep 3; Start-Process 'http://localhost:8011'"

echo FicheLab va s'ouvrir dans votre navigateur sur http://localhost:8011
echo.
echo  >> GARDEZ CETTE FENETRE OUVERTE pendant que vous travaillez.
echo  >> Pour arreter FicheLab : fermez cette fenetre ^(ou Ctrl+C^).
echo.

.venv\Scripts\python.exe -m uvicorn backend.app:app --port 8011

echo.
echo FicheLab s'est arrete.
pause
