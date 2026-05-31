import threading
import time

from pynput import keyboard as KeyboardManager
from pynput.mouse import Controller as MouseController

import modules.config as config


class SlotReader:
    def __init__(self, log=None, on_complete=None):
        self.log = log or (lambda message: None)
        self.on_complete = on_complete or (lambda result: None)
        self.mouse = MouseController()
        self.listener = None
        self.step = 0
        self.first_row = None
        self.drop = None
        self.difference = None
        self.result = None
        self.suppress_hotkeys_until = 0

    @property
    def is_running(self):
        return self.listener is not None

    @property
    def blocks_mining_hotkeys(self):
        return self.is_running or time.monotonic() < self.suppress_hotkeys_until

    def start(self):
        if self.is_running:
            self.log("Czytnik slotów już działa.")
            return

        self.step = 0
        self.first_row = None
        self.drop = None
        self.difference = None
        self.result = None
        self.listener = KeyboardManager.Listener(on_release=self._on_release)
        self.listener.start()
        self.log("Czytnik slotów uruchomiony. Ustaw mysz na slocie 1 i kliknij F8.")

    def cancel(self):
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
            self.suppress_hotkeys_until = time.monotonic() + 1
        self.log("Czytnik slotów anulowany.")

    def _on_release(self, key):
        if key != KeyboardManager.Key.f8:
            return

        if self.step == 0:
            self.first_row = self.mouse.position
            self.step = 1
            self.log("Slot 1 zapisany. Ustaw mysz na slocie 2 i kliknij F8.")
            return

        if self.step == 1:
            self.difference = self.mouse.position[0] - self.first_row[0]
            self.step = 2
            self.log("Odstęp slotów zapisany. Ustaw mysz poza ekwipunkiem w miejscu wyrzucania itemów i kliknij F8.")
            return

        self.drop = self.mouse.position
        self.result = {
            "first_row_x": self.first_row[0],
            "first_row_y": self.first_row[1],
            "drop_x": self.drop[0],
            "drop_y": self.drop[1],
            "difference": self.difference,
        }

        listener = self.listener
        self.listener = None
        self.suppress_hotkeys_until = time.monotonic() + 1
        if listener is not None:
            listener.stop()

        self.log("Pozycje zapisane. Test ruchu myszy rozpocznie się za 2 sekundy. Nie ruszaj myszą.")
        threading.Thread(target=self._test_and_complete, daemon=True).start()

    def _test_and_complete(self):
        time.sleep(2)
        self.test()
        time.sleep(1)
        self.log("Test czytnika slotów zakończony. Pozycje zostaną automatycznie zapisane w lokalnej konfiguracji użytkownika.")
        self.save_to_config()
        self.on_complete(self.result)

    def test(self):
        if self.result is None:
            return

        first_row = (self.result["first_row_x"], self.result["first_row_y"])
        difference = self.result["difference"]

        for row_index in range(4):
            for column_index in range(9):
                self.mouse.position = (
                    first_row[0] + (column_index * difference),
                    first_row[1] + (row_index * difference),
                )
                time.sleep(0.3)

    def save_to_config(self):
        if self.result is None:
            self.log("Brak zapisanych pozycji slotów.")
            return

        config.update_slots(self.result)
        self.log(f"Pozycje slotów zapisane do {config.CONFIG_PATH}.")
