#!/bin/bash

# Script para limpar pastas de build e recriar o executável

echo "Removendo pastas build e dist..."
rm -rf build dist

echo "Criando novo executável..."
python -m PyInstaller --onefile --console --icon icon.ico app.py

echo "Build concluído! Executável em dist/app.exe"