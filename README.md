# DriveSafe | Sistema de citas (Python)

Aplicación académica de consola para gestionar clientes, instructores, vehículos y citas. Los registros se almacenan en `Data/`.

## Abrir sin escribir comandos (Windows)

1. Descomprime **todo** el ZIP.
2. Abre la carpeta `DriveSafe_LISTO`.
3. Haz doble clic en **INICIAR_DRIVESAFE.bat**.
4. Elige las opciones del menú escribiendo números dentro de la ventana que se abre.

Requiere Python 3.10 o posterior instalado en Windows; no se necesitan librerías adicionales. El archivo BAT es un iniciador, no un ejecutable autónomo: necesita Python.

## Abrir desde Visual Studio Code

Abre **la carpeta `DriveSafe_LISTO` directamente** en VS Code: Archivo > Abrir carpeta. No abras únicamente `main.py` suelto. En este proyecto `.vscode/settings.json` configura Code Runner para ejecutar programas en la Terminal interactiva, no en Output. Puedes ejecutar `main.py` con el botón **Run Code**, o con **F5** si tienes la extensión Python Debugger. Si una configuración global interfiere, usa el archivo `INICIAR_DRIVESAFE.bat`.

## Registrar citas

Menú principal > **4. Módulo citas** > **3. Registrar cita**. Si el cliente no existe, se ofrece registrarlo en ese momento. El instructor y el vehículo deben estar registrados; su especialidad y tipo deben coincidir. Puedes probar con el cliente `323121`, instructor `43655`, placa `CTY45` (datos de ejemplo incluidos).

Las citas guardan fecha, hora, duración, asistencia y observaciones. El sistema valida solapamientos de horarios por instructor y vehículo.

## Datos y publicación

Los datos se guardan en `Data/*.json`, en la misma carpeta del proyecto. Al reemplazar versiones, respalda esta carpeta si ya agregaste registros. **Antes de publicar en GitHub, anonimiza documentos y datos personales en los JSON.**
