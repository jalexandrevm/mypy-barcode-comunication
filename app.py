import sys
from pathlib import Path

from config import AppConfig
from gui import PrinterApp
from logger import setup_logging
from printer import list_printers, send_raw_to_printer


def run_gui():
    app = PrinterApp()
    app.run()


def run_cli(file_path: str, printer_name: str):
    config = AppConfig("app.ini")
    setup_logging(config.get("log_file"))

    path = Path(file_path)
    if not path.exists() or not path.is_file():
        print(f"Error: file not found: {file_path}")
        sys.exit(1)

    available_printers = list_printers()
    if printer_name not in available_printers:
        print(f"Error: printer not found: {printer_name}")
        print("Installed printers:")
        for p in available_printers:
            print(f" - {p}")
        sys.exit(1)

    try:
        with path.open("rb") as f:
            raw_data = f.read()

        send_raw_to_printer(printer_name, raw_data)
        print(f"Sent file '{file_path}' to printer '{printer_name}'")
        config.set("default_printer", printer_name)
    except Exception as e:
        print(f"Error sending to printer: {e}")
        sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) == 2:
        file_name, printer_name = args
        run_cli(file_name, printer_name)
    else:
        run_gui()


if __name__ == "__main__":
    main()
