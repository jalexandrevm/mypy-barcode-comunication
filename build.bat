@echo off

REM Script para limpar pastas de build e recriar o executável

echo Removendo pastas build e dist...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Criando novo executável...
if exist icon.ico (
    python -m PyInstaller --onefile --console --icon icon.ico app.py
) else (
    echo Aviso: icon.ico não encontrado. Criando executável sem ícone.
    python -m PyInstaller --onefile --console app.py
)

echo Build concluído! Executável em dist\app.exe