# Printer Code Direct Sending

A simple Windows desktop app to send raw PPLA commands to a barcode printer via the Windows print spooler.

## Features

- `tkinter` GUI with a command editor
- raw printer communication using `pywin32`
- `app.ini` configuration file
- printer selection and default printer persistence
- file-based logging for debugging

## Setup

1. Create a virtual environment:

```sh
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

3. Run the app:

```sh
python app.py
```

## CLI mode

You can use the same script as an automated command tool with 2 arguments:

```sh
python app.py <path_to_ppla_file> "Printer Name"
```

The behavior is:
- reads raw PPLA command bytes from `<path_to_ppla_file>`
- checks that `Printer Name` exists in installed printers
- sends the bytes as RAW to the printer spooler
- updates `default_printer` in `app.ini`

Examples:

```sh
python app.py sample.ppla "Zebra ZD620"
python app.py C:\temp\label.txt "MyBarcodePrinter"
```

## Notes

- The app uses the Windows printer spooler. Make sure the barcode printer is installed as a Windows printer.
- The first time it runs, it detects the system default printer and saves it in `app.ini`.
- Use the `Refresh printers` button if installed printers change while the app is running.

## Executável

Para criar um executável standalone:

1. Instale PyInstaller: `pip install pyinstaller`
2. Execute o script de build: `build.bat` (Windows CMD/PowerShell) ou `./build.sh` (Git Bash/Linux)
3. O executável será gerado em `dist/app.exe`

### Ícone Personalizado

- Coloque um arquivo `icon.ico` na raiz do projeto para definir o ícone do executável e da janela da aplicação.
- Se `icon.ico` não existir, o build será feito sem ícone (com aviso).

### Uso do Executável

- GUI: Clique duas vezes em `app.exe` para abrir a interface gráfica.
- CLI: `app.exe <caminho_para_arquivo> "Nome da Impressora"`
