import threading
import time

from pynput import keyboard as KeyboardManager

import modules.config as config
from modules.input_backends import BACKGROUND_MODE
from modules.input_backends import FOREGROUND_MODE
from modules.input_backends import BackgroundInputError
from modules.input_backends import PynputInputBackend
from modules.input_backends import Win32WindowInputBackend


def mode_label(mode):
    return {
        FOREGROUND_MODE: "na pierwszym planie",
        BACKGROUND_MODE: "w tle",
    }.get(mode, mode)


class AfkController:
    def __init__(self, log=None):
        self.log = log or (lambda message: None)
        self.foreground_backend = PynputInputBackend()
        self.input = self.foreground_backend
        self.active_mode = FOREGROUND_MODE
        self.start_options = lambda: (FOREGROUND_MODE, None)
        self.mining = False
        self.fishing = False
        self.mobgrinder = False
        self.mining_thread = None
        self.activity_thread = None
        self.fishing_thread = None
        self.mobgrinder_thread = None
        self.mining_stop = threading.Event()
        self.activity_stop = threading.Event()
        self.fishing_stop = threading.Event()
        self.mobgrinder_stop = threading.Event()
        self.lock = threading.Lock()
        self.hotkey_listener = None
        self.slot_reader_active = lambda: False
        self.drop_skip_logged = False
        self._reset_rounds()

    def set_slot_reader_active(self, callback):
        self.slot_reader_active = callback

    def set_start_options(self, callback):
        self.start_options = callback

    def _reset_rounds(self):
        self.activity_rounds = 0
        self.cobblex_rounds = 0
        self.drop_rounds = 0
        self.eat_rounds = 0

    def release_all(self):
        self.input.release_all()

    def is_running(self):
        return self.mining or self.fishing or self.mobgrinder

    def active_activity_label(self):
        if self.mining:
            return "Kopanie"
        if self.fishing:
            return "Łowienie"
        if self.mobgrinder:
            return "Mobgrinder"
        return "Bezczynny"

    def start_hotkeys(self):
        if self.hotkey_listener is not None:
            return

        self.hotkey_listener = KeyboardManager.Listener(on_release=self._on_hotkey_release)
        self.hotkey_listener.start()

    def stop_hotkeys(self):
        if self.hotkey_listener is None:
            return
        self.hotkey_listener.stop()
        self.hotkey_listener = None

    def _on_hotkey_release(self, key):
        if self.slot_reader_active():
            return
        if key == KeyboardManager.Key.f8:
            mode, target_window = self.start_options()
            self.start_mining(mode=mode, target_window=target_window)
        elif key == KeyboardManager.Key.f9:
            self.stop()
        elif key == KeyboardManager.Key.f10:
            self.release_all()

    def start_mining(self, mode=FOREGROUND_MODE, target_window=None):
        with self.lock:
            if self.is_running():
                self.log(f"{self.active_activity_label()} AFK już działa. Zatrzymaj aktualny tryb przed uruchomieniem kopania.")
                return

            config.reload()
            self._reset_rounds()
            self.drop_skip_logged = False
            self.input = self._create_input_backend(mode, target_window)
            self.active_mode = self.input.mode
            self.mining_stop.clear()
            self.activity_stop.clear()
            self.mining = True

            self.mining_thread = threading.Thread(target=self._start_moving, daemon=True)
            self.activity_thread = threading.Thread(target=self._activity, daemon=True)
            self.mining_thread.start()
            self.activity_thread.start()

        self.log(f"Rozpoczęto kopanie AFK ({mode_label(self.active_mode)}).")

    def start_fishing(self, mode=FOREGROUND_MODE, target_window=None):
        with self.lock:
            if self.is_running():
                self.log(f"{self.active_activity_label()} AFK już działa. Zatrzymaj aktualny tryb przed uruchomieniem łowienia.")
                return

            self.input = self._create_input_backend(mode, target_window)
            self.active_mode = self.input.mode
            self.fishing_stop.clear()
            self.fishing = True

            self.fishing_thread = threading.Thread(target=self._start_fishing, daemon=True)
            self.fishing_thread.start()

        self.log(f"Rozpoczęto łowienie AFK ({mode_label(self.active_mode)}).")

    def start_mobgrinder(self, mode=FOREGROUND_MODE, target_window=None):
        with self.lock:
            if self.is_running():
                self.log(f"{self.active_activity_label()} AFK już działa. Zatrzymaj aktualny tryb przed uruchomieniem mobgrindera.")
                return

            config.reload()
            self.input = self._create_input_backend(mode, target_window)
            self.active_mode = self.input.mode
            self.mobgrinder_stop.clear()
            self.mobgrinder = True

            self.mobgrinder_thread = threading.Thread(target=self._start_mobgrinder, daemon=True)
            self.mobgrinder_thread.start()

        self.log(f"Rozpoczęto mobgrinder AFK ({mode_label(self.active_mode)}).")

    def _create_input_backend(self, mode, target_window):
        if mode != BACKGROUND_MODE:
            return self.foreground_backend

        if target_window is None:
            self.log("Nie wybrano okna do trybu w tle. Uruchamiam tryb na pierwszym planie.")
            return self.foreground_backend

        try:
            backend = Win32WindowInputBackend(target_window)
            backend.probe()
            self.log(f"Tryb w tle użyje okna: {target_window.title}")
            return backend
        except BackgroundInputError as exc:
            self.log(f"Tryb w tle jest niedostępny ({exc}). Uruchamiam tryb na pierwszym planie.")
            return self.foreground_backend

    def stop(self):
        with self.lock:
            if not self.mining and not self.fishing and not self.mobgrinder:
                self.release_all()
                self.log("AFK nie jest uruchomione.")
                return

            if self.mobgrinder:
                self.log("Zatrzymywanie mobgrinder AFK...")
                self.mobgrinder = False
                self.mobgrinder_stop.set()
                stopped_activity = "Mobgrinder"
                mobgrinder_thread = self.mobgrinder_thread
                fishing_thread = None
                mining_thread = None
                activity_thread = None
            elif self.fishing:
                self.log("Zatrzymywanie łowienia AFK...")
                self.fishing = False
                self.fishing_stop.set()
                stopped_activity = "Łowienie"
                mobgrinder_thread = None
                fishing_thread = self.fishing_thread
                mining_thread = None
                activity_thread = None
            else:
                self.log("Zatrzymywanie kopania AFK...")
                self.mining = False
                self.activity_stop.set()
                self.mining_stop.set()
                stopped_activity = "Kopanie"
                mobgrinder_thread = None
                mining_thread = self.mining_thread
                activity_thread = self.activity_thread
                fishing_thread = None

        self._join_thread(activity_thread)
        self._join_thread(mining_thread)
        self._join_thread(fishing_thread)
        self._join_thread(mobgrinder_thread)
        self.release_all()

        with self.lock:
            self.mining_thread = None
            self.activity_thread = None
            self.fishing_thread = None
            self.mobgrinder_thread = None
            self.input = self.foreground_backend
            self.active_mode = FOREGROUND_MODE
            self._reset_rounds()

        self.log(f"{stopped_activity} AFK zostało zatrzymane.")

    def _join_thread(self, thread):
        if thread and thread.is_alive() and thread is not threading.current_thread():
            thread.join()

    def _sleep(self, seconds, stop_event):
        return stop_event.wait(max(0, seconds))

    def _fail_active_run(self, message):
        self.log(message)
        with self.lock:
            self.mining = False
            self.fishing = False
            self.mobgrinder = False
        self.activity_stop.set()
        self.mining_stop.set()
        self.fishing_stop.set()
        self.mobgrinder_stop.set()

    def _start_moving(self):
        try:
            while not self.mining_stop.is_set():
                self.input.press_mouse("left")

                if config.fast_pickaxe:
                    horizontal_delay = (config.horizontal_stones / 4) - 0.2
                    vertical_delay = (config.vertical_stones / 4) - 0.2

                    self.input.press_key("d")
                    if self._sleep(horizontal_delay, self.mining_stop):
                        break
                    self.input.release_key("d")

                    if config.vertical_stones > 0:
                        self.input.press_key("w")
                        if self._sleep(vertical_delay, self.mining_stop):
                            break
                        self.input.release_key("w")

                    self.input.press_key("a")
                    if self._sleep(horizontal_delay, self.mining_stop):
                        break
                    self.input.release_key("a")

                    if config.vertical_stones > 0:
                        self.input.press_key("s")
                        if self._sleep(vertical_delay, self.mining_stop):
                            break
                        self.input.release_key("s")
                elif self._sleep(5, self.mining_stop):
                    break

                self.activity_rounds += 1
                self.cobblex_rounds += 1
                self.drop_rounds += 1
                self.eat_rounds += 1
        except BackgroundInputError as exc:
            self._fail_active_run(f"Tryb w tle został przerwany: {exc}")
        finally:
            self.release_all()

    def _start_fishing(self):
        try:
            self.input.press_mouse("right")
            while not self.fishing_stop.wait(0.1):
                pass
        except BackgroundInputError as exc:
            self._fail_active_run(f"Tryb w tle został przerwany: {exc}")
        finally:
            self.release_all()

    def _start_mobgrinder(self):
        try:
            while not self.mobgrinder_stop.is_set():
                self.input.click_mouse("left")
                if self.mobgrinder_stop.wait(config.mobgrinder_click_interval):
                    break
        except BackgroundInputError as exc:
            self._fail_active_run(f"Tryb w tle został przerwany: {exc}")
        finally:
            self.release_all()

    def _drop_slot(self, x, y):
        self.input.move_mouse(x, y)
        time.sleep(0.05)
        self.input.click_mouse("left")
        time.sleep(0.05)
        self.input.click_mouse("right")
        time.sleep(0.05)
        self.input.move_mouse(config.slots["drop_x"], config.slots["drop_y"])
        time.sleep(0.05)
        self.input.click_mouse("left")
        time.sleep(0.05)
        self.input.move_mouse(x, y)
        time.sleep(0.05)

    def _calculate_inventory_mouse_position(self, slot):
        rows = [
            range(1, 10),
            range(10, 19),
            range(19, 28),
            range(28, 37),
        ]

        for row_index, row in enumerate(rows):
            if slot in row:
                return (
                    config.slots["first_row_x"] + (list(row).index(slot) * config.slots["difference"]),
                    config.slots["first_row_y"] + (row_index * config.slots["difference"]),
                )

        raise ValueError(f"Nieprawidłowy slot ekwipunku: {slot}")

    def _drop(self):
        time.sleep(0.25)
        self.input.tap_key("e")
        time.sleep(0.25)

        for slot in [int(x) for x in config.drop_slots]:
            x, y = self._calculate_inventory_mouse_position(slot)
            self._drop_slot(x, y)

        time.sleep(0.25)
        self.input.tap_key("e")
        time.sleep(0.25)

    def _eat(self):
        time.sleep(0.1)
        self.input.tap_key(str(config.food))
        time.sleep(0.1)
        self.input.press_mouse("right")
        time.sleep(3)
        self.input.release_mouse("right")
        time.sleep(0.1)
        self.input.tap_key(str(config.pickaxe))

    def _send_command(self, command):
        self.input.release_mouse("right")
        self.input.tap_key("t")
        time.sleep(0.2)
        self.input.type_text(f"/{command}")
        self.input.tap_key("enter")
        time.sleep(config.commands_delay_in_seconds)

    def _activity(self):
        try:
            while not self.activity_stop.is_set():
                self._activity_step()
        except BackgroundInputError as exc:
            self._fail_active_run(f"Tryb w tle został przerwany: {exc}")

    def _activity_step(self):
        should_pause = (
            (config.enable_activity_commands and self.activity_rounds >= config.activity_rounds_config)
            or (config.enable_cobblex and self.cobblex_rounds >= config.cobblex_rounds_config)
            or (config.enable_dropping_items and self.drop_rounds >= config.drop_rounds_config)
            or (config.enable_eating and 1 <= config.food <= 9 and self.eat_rounds >= config.eat_rounds_config)
        )

        if not should_pause:
            self.activity_stop.wait(0.1)
            return

        self.mining_stop.set()
        self._join_thread(self.mining_thread)

        if self.activity_stop.is_set():
            return

        if config.enable_activity_commands and self.activity_rounds >= config.activity_rounds_config:
            for command in config.activity_commands:
                self._send_command(command)
            self.activity_rounds = 0

        if config.enable_cobblex and self.cobblex_rounds >= config.cobblex_rounds_config:
            for command in config.cobblex_commands:
                self._send_command(command)
            self.cobblex_rounds = 0

        if config.enable_dropping_items and self.drop_rounds >= config.drop_rounds_config:
            if self.active_mode == BACKGROUND_MODE:
                if not self.drop_skip_logged:
                    self.log("Wyrzucanie itemów jest dostępne tylko w trybie na pierwszym planie.")
                    self.drop_skip_logged = True
            else:
                self._drop()
            self.drop_rounds = 0

        if config.enable_eating and 1 <= config.food <= 9 and self.eat_rounds >= config.eat_rounds_config:
            self._eat()
            self.eat_rounds = 0

        if self.activity_stop.wait(1):
            return

        self.mining_stop.clear()
        self.mining_thread = threading.Thread(target=self._start_moving, daemon=True)
        self.mining_thread.start()
