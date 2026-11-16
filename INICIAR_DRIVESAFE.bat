@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title DriveSafe - Sistema de citas
where py >nul 2>nul
if not errorlevel 1 (
    py -3 "%~dp0main.py"
) else (
    where python >nul 2>nul
    if not errorlevel 1 (
        python "%~dp0main.py"
    ) else (
        echo ERROR: No se encontro Python 3 instalado.
        echo Instala Python desde python.org y habilita la opcion Add Python to PATH.
    )
)
echo.
echo DriveSafe ha finalizado. Presiona una tecla para cerrar esta ventana.
pause >nul
endlocal
