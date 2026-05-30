import threading
import time

from pynput import keyboard as KeyboardManager
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import modules.config as config


class MiningController:
    def __init__(self, log=None):
        self.log = log or (lambda message: None)
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.mining = False
        self.mining_thread = None
        self.activity_thread = None
        self.mining_stop = threading.Event()
        self.activity_stop = threading.Event()
        self.lock = threading.Lock()
        self.hotkey_listener = None
        self.slot_reader_active = lambda: False
        self._reset_rounds()

    def set_slot_reader_active(self, callback):
        self.slot_reader_active = callback

    def _reset_rounds(self):
        self.activity_rounds = 0
        self.cobblex_rounds = 0
        self.drop_rounds = 0
        self.eat_rounds = 0

    def release_all(self):
        self.mouse.release(Button.left)
        self.mouse.release(Button.right)
        for key in ("a", "d", "w", "s"):
            self.keyboard.release(key)

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
            self.start()
        elif key == KeyboardManager.Key.f9:
            self.stop()
        elif key == KeyboardManager.Key.f10:
            self.release_all()

    def start(self):
        with self.lock:
            if self.mining:
                self.log("Kopanie AFK już działa.")
                return

            config.reload()
            self._reset_rounds()
            self.mining_stop.clear()
            self.activity_stop.clear()
            self.mining = True

            self.mining_thread = threading.Thread(target=self._start_moving, daemon=True)
            self.activity_thread = threading.Thread(target=self._activity, daemon=True)
            self.mining_thread.start()
            self.activity_thread.start()

        self.log("Rozpoczęto kopanie AFK.")

    def stop(self):
        with self.lock:
            if not self.mining:
                self.release_all()
                self.log("Kopanie AFK nie jest uruchomione.")
                return

            self.log("Zatrzymywanie kopania AFK...")
            self.mining = False
            self.activity_stop.set()
            self.mining_stop.set()
            mining_thread = self.mining_thread
            activity_thread = self.activity_thread

        self._join_thread(activity_thread)
        self._join_thread(mining_thread)
        self.release_all()

        with self.lock:
            self.mining_thread = None
            self.activity_thread = None
            self._reset_rounds()

        self.log("Kopanie AFK zostało zatrzymane.")

    def _join_thread(self, thread):
        if thread and thread.is_alive() and thread is not threading.current_thread():
            thread.join()

    def _sleep(self, seconds, stop_event):
        return stop_event.wait(max(0, seconds))

    def _start_moving(self):
        while not self.mining_stop.is_set():
            self.mouse.press(Button.left)

            if config.fast_pickaxe:
                horizontal_delay = (config.horizontal_stones / 4) - 0.2
                vertical_delay = (config.vertical_stones / 4) - 0.2

                self.keyboard.press("d")
                if self._sleep(horizontal_delay, self.mining_stop):
                    break
                self.keyboard.release("d")

                if config.vertical_stones > 0:
                    self.keyboard.press("w")
                    if self._sleep(vertical_delay, self.mining_stop):
                        break
                    self.keyboard.release("w")

                self.keyboard.press("a")
                if self._sleep(horizontal_delay, self.mining_stop):
                    break
                self.keyboard.release("a")

                if config.vertical_stones > 0:
                    self.keyboard.press("s")
                    if self._sleep(vertical_delay, self.mining_stop):
                        break
                    self.keyboard.release("s")
            elif self._sleep(5, self.mining_stop):
                break

            self.activity_rounds += 1
            self.cobblex_rounds += 1
            self.drop_rounds += 1
            self.eat_rounds += 1

        self.release_all()

    def _drop_slot(self, x, y):
        self.mouse.position = (x, y)
        time.sleep(0.05)
        self.mouse.click(Button.left)
        time.sleep(0.05)
        self.mouse.click(Button.right)
        time.sleep(0.05)
        self.mouse.position = (config.slots["drop_x"], config.slots["drop_y"])
        time.sleep(0.05)
        self.mouse.click(Button.left)
        time.sleep(0.05)
        self.mouse.position = (x, y)
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
        self.keyboard.press("e")
        self.keyboard.release("e")
        time.sleep(0.25)

        for slot in [int(x) for x in config.drop_slots]:
            x, y = self._calculate_inventory_mouse_position(slot)
            self._drop_slot(x, y)

        time.sleep(0.25)
        self.keyboard.press("e")
        self.keyboard.release("e")
        time.sleep(0.25)

    def _eat(self):
        time.sleep(0.1)
        self.keyboard.press(str(config.food))
        self.keyboard.release(str(config.food))
        time.sleep(0.1)
        self.mouse.press(Button.right)
        time.sleep(3)
        self.mouse.release(Button.right)
        time.sleep(0.1)
        self.keyboard.press(str(config.pickaxe))
        self.keyboard.release(str(config.pickaxe))

    def _send_command(self, command):
        self.mouse.release(Button.right)
        self.keyboard.press("t")
        self.keyboard.release("t")
        time.sleep(0.2)
        self.keyboard.press("/")
        self.keyboard.release("/")
        time.sleep(0.2)
        self.keyboard.type(command)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(config.commands_delay_in_seconds)

    def _activity(self):
        while not self.activity_stop.is_set():
            should_pause = (
                self.activity_rounds >= config.activity_rounds_config
                or self.cobblex_rounds >= config.cobblex_rounds_config
                or self.drop_rounds >= config.drop_rounds_config
                or (1 <= config.food <= 9 and self.eat_rounds >= config.eat_rounds_config)
            )

            if not should_pause:
                self.activity_stop.wait(0.1)
                continue

            self.mining_stop.set()
            self._join_thread(self.mining_thread)

            if self.activity_stop.is_set():
                break

            if self.activity_rounds >= config.activity_rounds_config:
                for command in config.activity_commands:
                    self._send_command(command)
                self.activity_rounds = 0

            if self.cobblex_rounds >= config.cobblex_rounds_config:
                for command in config.cobblex_commands:
                    self._send_command(command)
                self.cobblex_rounds = 0

            if self.drop_rounds >= config.drop_rounds_config:
                self._drop()
                self.drop_rounds = 0

            if 1 <= config.food <= 9 and self.eat_rounds >= config.eat_rounds_config:
                self._eat()
                self.eat_rounds = 0

            if self.activity_stop.wait(1):
                break

            self.mining_stop.clear()
            self.mining_thread = threading.Thread(target=self._start_moving, daemon=True)
            self.mining_thread.start()
