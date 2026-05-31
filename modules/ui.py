import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk

import modules.check_version as check_version
import modules.config as config
from modules.input_backends import BACKGROUND_MODE
from modules.input_backends import FOREGROUND_MODE
from modules.input_backends import enumerate_windows
from modules.input_backends import find_minecraft_window
from modules.input_backends import is_background_input_supported
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
        self.geometry("760x740")
        self.minsize(680, 680)
        self.log_queue = queue.Queue()
        self.mode_var = tk.StringVar(value=FOREGROUND_MODE)
        self.window_var = tk.StringVar()
        self.window_targets = []
        self.window_by_display = {}
        self.background_available = is_background_input_supported()

        try:
            self.iconbitmap(default=str(resource_path("pickaxe.ico")))
        except tk.TclError:
            pass

        self.mining = MiningController(log=self.log)
        self.slot_reader = SlotReader(log=self.log, on_complete=self.on_slot_reader_complete)
        self.mining.set_slot_reader_active(lambda: self.slot_reader.blocks_mining_hotkeys)
        self.mining.set_start_options(self._selected_start_options)

        self._build_ui()
        self._refresh_window_targets(log_result=False)
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
        controls.columnconfigure(4, weight=1)

        ttk.Label(controls, text="Tryb:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Radiobutton(
            controls,
            text="Na pierwszym planie",
            value=FOREGROUND_MODE,
            variable=self.mode_var,
            command=self._on_mode_changed,
        ).grid(row=0, column=1, sticky="w", padx=(0, 8))
        self.background_radio = ttk.Radiobutton(
            controls,
            text="W tle",
            value=BACKGROUND_MODE,
            variable=self.mode_var,
            command=self._on_mode_changed,
        )
        self.background_radio.grid(row=0, column=2, sticky="w", padx=(0, 8))
        if not self.background_available:
            self.background_radio.configure(state="disabled")

        self.status_label = ttk.Label(controls, text="Bezczynny")
        self.status_label.grid(row=0, column=4, sticky="e")

        ttk.Button(controls, text="Uruchom AFK", command=self._start_mining).grid(row=1, column=0, padx=(0, 8), pady=(10, 0))
        ttk.Button(controls, text="Zatrzymaj", command=self._stop_mining_async).grid(row=1, column=1, padx=(0, 8), pady=(10, 0))
        self.target_label = ttk.Label(controls, text="Okno:")
        self.target_combo = ttk.Combobox(controls, textvariable=self.window_var, state="readonly", width=48)
        self.target_refresh = ttk.Button(controls, text="Odśwież", command=self._refresh_window_targets)
        self.target_label.grid(row=2, column=0, sticky="w", pady=(10, 0), padx=(0, 8))
        self.target_combo.grid(row=2, column=1, columnspan=3, sticky="ew", pady=(10, 0), padx=(0, 8))
        self.target_refresh.grid(row=2, column=4, sticky="e", pady=(10, 0))
        self.target_widgets = [self.target_label, self.target_combo, self.target_refresh]
        self._on_mode_changed()

        content = ttk.Frame(self, padding=(16, 0, 16, 8))
        content.grid(row=2, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=0)
        content.rowconfigure(1, weight=1, minsize=240)

        config_frame = ttk.LabelFrame(content, text="Aktualna konfiguracja", padding=12)
        config_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)
        config_frame.columnconfigure(0, weight=1)
        self.config_summary_values = {}
        self.config_summary_state_labels = {}
        self._build_config_summary(config_frame)
        button_bar = ttk.Frame(config_frame)
        button_bar.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(button_bar, text="Odśwież konfigurację", command=self._refresh_config_summary).grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Button(button_bar, text="Edytuj konfigurację", command=self._open_config_form).grid(row=0, column=1, sticky="w")

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
            text="Po zakończeniu testu pozycje zostaną zapisane automatycznie w lokalnej konfiguracji użytkownika.",
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

    def _on_mode_changed(self):
        visible = self.mode_var.get() == BACKGROUND_MODE
        for widget in self.target_widgets:
            if visible:
                widget.grid()
            else:
                widget.grid_remove()

        if visible and not self.window_targets:
            self._refresh_window_targets(log_result=False)

    def _refresh_window_targets(self, log_result=True):
        if not self.background_available:
            self.window_targets = []
            self.window_by_display = {}
            self.target_combo.configure(values=())
            self.window_var.set("")
            if log_result:
                self.log("Tryb w tle jest dostępny tylko na Windows z pywin32.")
            return

        self.window_targets = enumerate_windows()
        self.window_by_display = {window.display_name: window for window in self.window_targets}
        values = list(self.window_by_display.keys())
        self.target_combo.configure(values=values)

        selected = find_minecraft_window(self.window_targets)
        self.window_var.set(selected.display_name if selected else "")

        if log_result:
            self.log(f"Odświeżono listę okien ({len(self.window_targets)}).")

    def _selected_start_options(self):
        mode = self.mode_var.get()
        if mode != BACKGROUND_MODE:
            return FOREGROUND_MODE, None
        return BACKGROUND_MODE, self._selected_window_target()

    def _selected_window_target(self):
        return self.window_by_display.get(self.window_var.get())

    def _start_mining(self):
        mode, target_window = self._selected_start_options()
        self.mining.start(mode=mode, target_window=target_window)

    def log(self, message):
        self.log_queue.put(message)

    def _poll_logs(self):
        while True:
            try:
                message = self.log_queue.get_nowait()
            except queue.Empty:
                break
            self._append_log(message)

        if self.mining.mining:
            self.status_label.configure(text=f"Działa ({self._mode_label(self.mining.active_mode)})")
        else:
            self.status_label.configure(text="Bezczynny")
        self.after(100, self._poll_logs)

    def _mode_label(self, mode):
        return {
            FOREGROUND_MODE: "na pierwszym planie",
            BACKGROUND_MODE: "w tle",
        }.get(mode, mode)

    def _append_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"MineAFK - {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _build_config_summary(self, parent):
        summary = ttk.Frame(parent)
        summary.grid(row=0, column=0, sticky="ew")
        summary.columnconfigure(1, weight=1)

        rows = [
            ("stones", "Stoniarki:", "value"),
            ("enable_eating", "Jedzenie:", "state"),
            ("enable_dropping_items", "Wyrzucanie itemów:", "state"),
            ("enable_activity_commands", "Aktywność:", "state"),
            ("enable_cobblex", "Cobblex:", "state"),
            ("activity_commands", "Komendy aktywności:", "value"),
            ("cobblex_commands", "Komendy cobblex:", "value"),
        ]

        for row_index, (key, label, row_type) in enumerate(rows):
            ttk.Label(summary, text=label).grid(row=row_index, column=0, sticky="nw", padx=(0, 8), pady=1)
            value_label = ttk.Label(summary, wraplength=240, justify="left")
            value_label.grid(row=row_index, column=1, sticky="ew", pady=1)
            self.config_summary_values[key] = value_label
            if row_type == "state":
                self.config_summary_state_labels[key] = value_label

    def _open_config_form(self):
        existing_editor = getattr(self, "config_editor", None)
        if existing_editor is not None and existing_editor.winfo_exists():
            existing_editor.lift()
            existing_editor.focus_force()
            return

        editor = tk.Toplevel(self)
        self.config_editor = editor
        editor.title("MineAFK - konfiguracja")
        editor.geometry("700x620")
        editor.minsize(560, 420)
        editor.transient(self)
        editor.columnconfigure(0, weight=1)
        editor.rowconfigure(1, weight=1)

        header = ttk.Frame(editor, padding=(12, 12, 12, 6))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text=f"Plik: {config.CONFIG_PATH}", wraplength=660).grid(row=0, column=0, sticky="w")

        canvas = tk.Canvas(editor, borderwidth=0, highlightthickness=0)
        canvas.grid(row=1, column=0, sticky="nsew", padx=(12, 0), pady=(0, 8))
        y_scrollbar = ttk.Scrollbar(editor, orient="vertical", command=canvas.yview)
        y_scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 8))
        canvas.configure(yscrollcommand=y_scrollbar.set)

        def scroll_form(event):
            if getattr(event, "num", None) == 4:
                canvas.yview_scroll(-3, "units")
            elif getattr(event, "num", None) == 5:
                canvas.yview_scroll(3, "units")
            elif event.delta:
                steps = int(-1 * (event.delta / 120))
                if steps == 0:
                    steps = -1 if event.delta > 0 else 1
                canvas.yview_scroll(steps, "units")
            return "break"

        editor.bind("<MouseWheel>", scroll_form)
        editor.bind("<Button-4>", scroll_form)
        editor.bind("<Button-5>", scroll_form)

        form = ttk.Frame(canvas, padding=(0, 0, 12, 0))
        form_window = canvas.create_window((0, 0), window=form, anchor="nw")
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(form_window, width=event.width))
        form.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        form.columnconfigure(0, weight=1)

        fields = {}
        bool_fields = {}
        entry_widgets = {}
        controlled_fields = {
            "enable_eating": ["eat_rounds", "food"],
            "enable_dropping_items": ["drop_rounds", "drop_slots", "first_row_x", "first_row_y", "drop_x", "drop_y", "difference"],
            "enable_activity_commands": ["activity_rounds", "activity_commands"],
            "enable_cobblex": ["cobblex_rounds", "cobblex_commands"],
        }

        def update_field_states():
            for toggle_key, field_keys in controlled_fields.items():
                enabled = bool_fields[toggle_key].get()
                state = "normal" if enabled else "disabled"
                for field_key in field_keys:
                    widget = entry_widgets.get(field_key)
                    if widget is not None:
                        widget.configure(state=state)

        def current_values():
            config.reload()
            return {
                "horizontal_stones": str(config.horizontal_stones),
                "vertical_stones": str(config.vertical_stones),
                "pickaxe": str(config.pickaxe),
                "eat_rounds": str(config.eat_rounds_config),
                "food": str(config.food),
                "drop_rounds": str(config.drop_rounds_config),
                "drop_slots": ",".join(config.drop_slots),
                "activity_rounds": str(config.activity_rounds_config),
                "activity_commands": ",".join(config.activity_commands),
                "cobblex_rounds": str(config.cobblex_rounds_config),
                "cobblex_commands": ",".join(config.cobblex_commands),
                "commands_delay_in_seconds": str(config.commands_delay_in_seconds),
                "fast_pickaxe": config.fast_pickaxe,
                "enable_eating": config.enable_eating,
                "enable_dropping_items": config.enable_dropping_items,
                "enable_activity_commands": config.enable_activity_commands,
                "enable_cobblex": config.enable_cobblex,
                "first_row_x": str(config.slots["first_row_x"]),
                "first_row_y": str(config.slots["first_row_y"]),
                "drop_x": str(config.slots["drop_x"]),
                "drop_y": str(config.slots["drop_y"]),
                "difference": str(config.slots["difference"]),
            }

        sections = [
            (
                "Funkcje",
                [
                    ("enable_eating", "Jedzenie", "bool"),
                    ("enable_dropping_items", "Wyrzucanie itemów", "bool"),
                    ("enable_activity_commands", "Komendy aktywności", "bool"),
                    ("enable_cobblex", "Cobblex", "bool"),
                ],
            ),
            (
                "Config",
                [
                    ("horizontal_stones", "Stoniarki w szerokości", "entry"),
                    ("vertical_stones", "Stoniarki przód/tył", "entry"),
                    ("pickaxe", "Slot kilofa (1-9)", "entry"),
                    ("eat_rounds", "Rundy jedzenia", "entry"),
                    ("food", "Slot jedzenia (0-9)", "entry"),
                    ("drop_rounds", "Rundy wyrzucania", "entry"),
                    ("drop_slots", "Sloty do wyrzucenia (1-36, po przecinku)", "entry"),
                    ("activity_rounds", "Rundy aktywności", "entry"),
                    ("activity_commands", "Komendy aktywności (po przecinku)", "entry"),
                    ("cobblex_rounds", "Rundy cobblex", "entry"),
                    ("cobblex_commands", "Komendy cobblex (po przecinku)", "entry"),
                    ("commands_delay_in_seconds", "Odstęp między komendami w sekundach", "entry"),
                    ("fast_pickaxe", "Szybki kilof", "bool"),
                ],
            ),
            (
                "Slots",
                [
                    ("first_row_x", "Slot 1 X", "entry"),
                    ("first_row_y", "Slot 1 Y", "entry"),
                    ("drop_x", "Miejsce wyrzucania X", "entry"),
                    ("drop_y", "Miejsce wyrzucania Y", "entry"),
                    ("difference", "Odstęp slotów", "entry"),
                ],
            ),
        ]

        try:
            values = current_values()
        except Exception as exc:
            messagebox.showerror("MineAFK", f"Nie udało się odczytać konfiguracji:\n{exc}", parent=editor)
            editor.destroy()
            return
        first_entry = None
        for row_index, (section_name, section_fields) in enumerate(sections):
            section = ttk.LabelFrame(form, text=section_name, padding=12)
            section.grid(row=row_index, column=0, sticky="ew", pady=(0, 10))
            section.columnconfigure(1, weight=1)

            for field_row, (key, label, field_type) in enumerate(section_fields):
                ttk.Label(section, text=label).grid(row=field_row, column=0, sticky="w", padx=(0, 12), pady=4)
                if field_type == "bool":
                    variable = tk.BooleanVar(value=bool(values[key]))
                    bool_fields[key] = variable
                    command = update_field_states if key in controlled_fields else None
                    ttk.Checkbutton(section, variable=variable, command=command).grid(row=field_row, column=1, sticky="w", pady=4)
                else:
                    variable = tk.StringVar(value=values[key])
                    fields[key] = variable
                    entry = ttk.Entry(section, textvariable=variable)
                    entry_widgets[key] = entry
                    entry.grid(row=field_row, column=1, sticky="ew", pady=4)
                    first_entry = first_entry or entry

        def load_from_disk():
            try:
                values_from_disk = current_values()
            except Exception as exc:
                messagebox.showerror("MineAFK", f"Nie udało się odczytać konfiguracji:\n{exc}", parent=editor)
                return

            for key, variable in fields.items():
                variable.set(values_from_disk[key])
            for key, variable in bool_fields.items():
                variable.set(bool(values_from_disk[key]))
            update_field_states()

        def collect_values():
            values_to_save = {key: variable.get() for key, variable in fields.items()}
            values_to_save.update({key: variable.get() for key, variable in bool_fields.items()})
            return values_to_save

        def save_to_disk():
            try:
                config.save_config_values(collect_values())
            except Exception as exc:
                messagebox.showerror("MineAFK", f"Nie udało się zapisać konfiguracji:\n{exc}", parent=editor)
                return

            self._refresh_config_summary()
            self.log(f"Konfiguracja została zapisana w {config.CONFIG_PATH}.")
            editor.destroy()

        actions = ttk.Frame(editor, padding=(12, 0, 12, 12))
        actions.grid(row=2, column=0, columnspan=2, sticky="ew")
        actions.columnconfigure(0, weight=1)
        ttk.Button(actions, text="Wczytaj ponownie", command=load_from_disk).grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Button(actions, text="Zapisz", command=save_to_disk).grid(row=0, column=1, sticky="e", padx=(0, 8))
        ttk.Button(actions, text="Anuluj", command=editor.destroy).grid(row=0, column=2, sticky="e")

        update_field_states()
        if first_entry is not None:
            first_entry.focus_set()

    def _refresh_config_summary(self):
        config.reload()
        self.config_summary_values["stones"].configure(text=f"{config.horizontal_stones} x {config.vertical_stones}")
        self._set_summary_state("enable_eating", config.enable_eating)
        self._set_summary_state("enable_dropping_items", config.enable_dropping_items)
        self._set_summary_state("enable_activity_commands", config.enable_activity_commands)
        self._set_summary_state("enable_cobblex", config.enable_cobblex)
        self.config_summary_values["activity_commands"].configure(text=", ".join(config.activity_commands) or "-")
        self.config_summary_values["cobblex_commands"].configure(text=", ".join(config.cobblex_commands) or "-")
        self.log("Konfiguracja została odświeżona.")

    def _set_summary_state(self, key, enabled):
        self.config_summary_state_labels[key].configure(
            text=self._enabled_label(enabled),
            foreground="#16803a" if enabled else "#b42318",
        )

    def _enabled_label(self, enabled):
        return "włączone" if enabled else "wyłączone"

    def _stop_mining_async(self):
        threading.Thread(target=self.mining.stop, daemon=True).start()

    def on_slot_reader_complete(self, result):
        self.after(0, self._refresh_after_slot_reader)

    def _refresh_after_slot_reader(self):
        self._refresh_config_summary()
        self.log(f"Czytnik slotów zakończył pracę. Konfiguracja została zaktualizowana w {config.CONFIG_PATH}.")

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
