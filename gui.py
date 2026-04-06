import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from config import AppConfig
from logger import setup_logging
from printer import get_default_printer, list_printers, send_raw_to_printer


class PrinterApp:
    def __init__(self):
        self.config = AppConfig("app.ini")
        self.logger = setup_logging(self.config.get("log_file"))
        self.root = tk.Tk()
        try:
            self.root.iconbitmap('icon.ico')
        except tk.TclError:
            pass
        self.root.title(self.config.get("app_name"))
        self._build_ui()
        self._load_printers()

    def _build_ui(self):
        width = self.config.get_int("window_width", 900)
        height = self.config.get_int("window_height", 600)
        x = self.config.get_int("window_x", 100)
        y = self.config.get_int("window_y", 100)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        top_frame = ttk.Frame(self.root, padding=12)
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.columnconfigure(1, weight=1)

        ttk.Label(top_frame, text="Printer:").grid(row=0, column=0, sticky="w")
        self.printer_var = tk.StringVar()
        self.printer_combo = ttk.Combobox(
            top_frame,
            textvariable=self.printer_var,
            state="readonly",
            postcommand=self._refresh_printer_list,
        )
        self.printer_combo.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        refresh_button = ttk.Button(top_frame, text="Refresh printers", command=self._refresh_printer_list)
        refresh_button.grid(row=0, column=2, sticky="e", padx=(8, 0))

        self.send_button = ttk.Button(self.root, text="Send to Printer", command=self.on_send)
        self.send_button.grid(row=3, column=0, pady=(8, 12), sticky="ew", padx=12)

        self.text_frame = ttk.Frame(self.root)
        self.text_frame.grid(row=1, column=0, sticky="nsew", padx=12)
        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.rowconfigure(0, weight=1)

        self.command_text = tk.Text(self.text_frame, wrap="none", undo=True)
        self.command_text.grid(row=0, column=0, sticky="nsew")

        vertical_scroll = ttk.Scrollbar(self.text_frame, orient="vertical", command=self.command_text.yview)
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll = ttk.Scrollbar(self.text_frame, orient="horizontal", command=self.command_text.xview)
        horizontal_scroll.grid(row=1, column=0, sticky="ew")

        self.command_text.configure(yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set)

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_label.grid(row=4, column=0, sticky="ew")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _load_printers(self):
        try:
            printers = list_printers()
            if not printers:
                raise RuntimeError("No printers were found on this system.")

            self.printer_combo["values"] = printers
            stored_printer = self.config.get("default_printer")
            system_default = get_default_printer() or ""
            if stored_printer and stored_printer in printers:
                self.printer_var.set(stored_printer)
            elif system_default and system_default in printers:
                self.printer_var.set(system_default)
                self.config.set("default_printer", system_default)
            else:
                self.printer_var.set(printers[0])
                self.config.set("default_printer", printers[0])

            self.status_var.set(f"Selected printer: {self.printer_var.get()}")
        except Exception as exc:
            self.logger.error("Failed to load printer list: %s", exc)
            messagebox.showerror("Printer Error", f"Unable to load installed printers.\n{exc}")
            self.printer_combo["values"] = []
            self.printer_var.set("")
            self.send_button.state(["disabled"])
            self.status_var.set("No printers available.")

    def _refresh_printer_list(self):
        try:
            printers = list_printers()
            self.printer_combo["values"] = printers
            if printers and not self.printer_var.get():
                self.printer_var.set(printers[0])
            self.status_var.set("Printer list refreshed.")
        except Exception as exc:
            self.logger.error("Failed to refresh printer list: %s", exc)
            messagebox.showerror("Printer Error", f"Unable to refresh printer list.\n{exc}")

    def on_send(self):
        commands = self.command_text.get("1.0", "end-1c")
        if not commands.strip():
            messagebox.showwarning("Empty Command", "Enter PPLA commands before sending.")
            return

        printer_name = self.printer_var.get()
        if not printer_name:
            messagebox.showerror("Printer Selection", "Select a printer before sending.")
            return

        self.config.set("default_printer", printer_name)
        self.logger.info("Sending commands to printer: %s", printer_name)

        try:
            encoding = self.config.get("encoding") or "utf-8"
            payload = commands.encode(encoding)
            send_raw_to_printer(printer_name, payload)
            self.status_var.set(f"Commands sent to: {printer_name}")
            messagebox.showinfo("Sent", f"Commands were sent to printer:\n{printer_name}")
        except Exception as exc:
            self.logger.exception("Failed to send data to printer")
            messagebox.showerror("Send Failed", f"Could not send commands to printer.\n{exc}")
            self.status_var.set("Send failed. See log for details.")

    def on_close(self):
        geometry = self.root.winfo_geometry().split("+")
        size = geometry[0].split("x")
        if len(size) == 2:
            self.config.set("window_width", size[0])
            self.config.set("window_height", size[1])
        if len(geometry) == 3:
            self.config.set("window_x", geometry[1])
            self.config.set("window_y", geometry[2])

        self.logger.info("Application closing")
        self.root.destroy()

    def run(self):
        self.logger.info("Application started")
        self.root.mainloop()
