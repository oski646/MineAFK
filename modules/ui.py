import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk

import modules.check_version as check_version
import modules.config as config
from modules.mining_controller import MiningController
from modules.slot_reader import SlotReader


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent.parent / relative_path


class MineAfkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MineAFK")
        self.geometry("760x700")
        self.minsize(680, 640)
        self.log_queue = queue.Queue()

        try:
            self.iconbitmap(default=str(resource_path("pickaxe.ico")))
        except tk.TclError:
            pass

        self.mining = MiningController(log=self.log)
        self.slot_reader = SlotReader(log=self.log, on_complete=self.on_slot_reader_complete)
        self.mining.set_slot_reader_active(lambda: self.slot_reader.blocks_mining_hotkeys)

        self._build_ui()
        self._refresh_config_summary()
        self._poll_logs()
        self.mining.start_hotkeys()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.log("Gotowe. Kliknij Uruchom AFK lub F8, aby rozpocząć. Kliknij Zatrzymaj lub F9, aby zatrzymać.")

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self, padding=(16, 14, 16, 8))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="MineAFK", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Lekki panel do kopania AFK i konfiguracji slotów.").grid(row=1, column=0, sticky="w")

        controls = ttk.LabelFrame(self, text="Sterowanie AFK", padding=12)
        controls.grid(row=1, column=0, sticky="ew", padx=16, pady=8)
        controls.columnconfigure(3, weight=1)

        ttk.Button(controls, text="Uruchom AFK", command=self.mining.start).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(controls, text="Zatrzymaj", command=self._stop_mining_async).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(controls, text="Zwolnij klawisze", command=self._release_keys).grid(row=0, column=2, padx=(0, 8))
        self.status_label = ttk.Label(controls, text="Bezczynny")
        self.status_label.grid(row=0, column=3, sticky="e")

        content = ttk.Frame(self, padding=(16, 0, 16, 8))
        content.grid(row=2, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=0)
        content.rowconfigure(1, weight=1, minsize=240)

        config_frame = ttk.LabelFrame(content, text="Aktualna konfiguracja", padding=12)
        config_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)
        config_frame.columnconfigure(0, weight=1)
        self.config_summary = ttk.Label(config_frame, justify="left")
        self.config_summary.grid(row=0, column=0, sticky="nw")
        ttk.Button(config_frame, text="Odśwież konfigurację", command=self._refresh_config_summary).grid(row=1, column=0, sticky="w", pady=(10, 0))

        slot_frame = ttk.LabelFrame(content, text="Czytnik slotów", padding=12)
        slot_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=8)
        slot_frame.columnconfigure(0, weight=1)
        slot_frame.columnconfigure(1, weight=1)
        ttk.Label(
            slot_frame,
            text="Użyj F8, aby zapisać slot 1, slot 2, a potem miejsce wyrzucania itemów.",
            wraplength=240,
            justify="left",
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Button(slot_frame, text="Start czytnika", command=self.slot_reader.start).grid(row=1, column=0, sticky="ew", pady=(10, 0), padx=(0, 6))
        ttk.Button(slot_frame, text="Anuluj", command=self.slot_reader.cancel).grid(row=1, column=1, sticky="ew", pady=(10, 0))
        ttk.Label(
            slot_frame,
            text="Po zakończeniu testu pozycje zostaną zapisane automatycznie do config.ini.",
            wraplength=240,
            justify="left",
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        logs_frame = ttk.LabelFrame(content, text="Logi", padding=12)
        logs_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(8, 0))
        logs_frame.configure(height=240)
        logs_frame.grid_propagate(False)
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(
            logs_frame,
            height=8,
            wrap="word",
            state="disabled",
            font=("Consolas", 10),
            padx=8,
            pady=6,
            relief="solid",
            borderwidth=1,
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(logs_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

        footer = ttk.Frame(self, padding=(16, 0, 16, 12))
        footer.grid(row=3, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)
        ttk.Button(footer, text="Sprawdź aktualizacje", command=self._check_updates_async).grid(row=0, column=0, sticky="w")

    def log(self, message):
        self.log_queue.put(message)

    def _poll_logs(self):
        while True:
            try:
                message = self.log_queue.get_nowait()
            except queue.Empty:
                break
            self._append_log(message)

        self.status_label.configure(text="Działa" if self.mining.mining else "Bezczynny")
        self.after(100, self._poll_logs)

    def _append_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"MineAFK - {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _refresh_config_summary(self):
        config.reload()
        self.config_summary.configure(
            text=(
                f"Wersja: {config.version}\n"
                f"Stoniarki: {config.horizontal_stones} x {config.vertical_stones}\n"
                f"Slot kilofa: {config.pickaxe}\n"
                f"Slot jedzenia: {config.food}\n"
                f"Sloty do wyrzucenia: {', '.join(config.drop_slots)}\n"
                f"Komendy aktywności: {', '.join(config.activity_commands)}\n"
                f"Komendy cobblex: {', '.join(config.cobblex_commands)}\n"
                f"Slot 1: {config.slots['first_row_x']}, {config.slots['first_row_y']}\n"
                f"Miejsce wyrzucania: {config.slots['drop_x']}, {config.slots['drop_y']}\n"
                f"Odstęp slotów: {config.slots['difference']}"
            )
        )
        self.log("Konfiguracja została odświeżona.")

    def _stop_mining_async(self):
        threading.Thread(target=self.mining.stop, daemon=True).start()

    def _release_keys(self):
        self.mining.release_all()
        self.log("Zwolniono przytrzymane klawisze ruchu i przyciski myszy.")

    def on_slot_reader_complete(self, result):
        self.after(0, self._refresh_after_slot_reader)

    def _refresh_after_slot_reader(self):
        self._refresh_config_summary()
        self.log("Czytnik slotów zakończył pracę. Config.ini został zaktualizowany automatycznie.")

    def _check_updates_async(self):
        threading.Thread(target=self._check_updates, daemon=True).start()

    def _check_updates(self):
        try:
            check_version.run(log=self.log)
            self.log("Sprawdzanie aktualizacji zakończone.")
        except Exception as exc:
            self.log(f"Nie udało się sprawdzić aktualizacji: {exc}")

    def _on_close(self):
        if self.mining.mining:
            if not messagebox.askyesno("MineAFK", "Kopanie AFK jest uruchomione. Zatrzymać je i zamknąć MineAFK?"):
                return
            self.mining.stop()

        self.slot_reader.cancel()
        self.mining.stop_hotkeys()
        self.destroy()


def run():
    app = MineAfkApp()
    app.mainloop()
