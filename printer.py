import logging

try:
    import win32print
except ImportError:  # pragma: no cover
    win32print = None

logger = logging.getLogger("printer_app")


def _ensure_win32print():
    if win32print is None:
        raise ImportError(
            "pywin32 is required to communicate with Windows printers. "
            "Install it with: pip install pywin32"
        )


def list_printers() -> list[str]:
    _ensure_win32print()
    flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    printers = win32print.EnumPrinters(flags)
    return [printer[2] for printer in printers if printer[2]]


def get_default_printer() -> str | None:
    _ensure_win32print()
    try:
        return win32print.GetDefaultPrinter()
    except Exception as exc:
        logger.debug("Unable to read default printer: %s", exc)
        return None


def send_raw_to_printer(printer_name: str, raw_data: bytes) -> None:
    _ensure_win32print()
    if not printer_name:
        raise ValueError("Printer name must be provided.")

    logger.debug("Opening printer: %s", printer_name)
    handle = win32print.OpenPrinter(printer_name)
    try:
        job_info = ("Printer Code Direct Sending", None, "RAW")
        logger.debug("Starting raw print job: %s", job_info)
        h_job = win32print.StartDocPrinter(handle, 1, job_info)
        try:
            win32print.StartPagePrinter(handle)
            win32print.WritePrinter(handle, raw_data)
            win32print.EndPagePrinter(handle)
        finally:
            win32print.EndDocPrinter(handle)
    finally:
        win32print.ClosePrinter(handle)
