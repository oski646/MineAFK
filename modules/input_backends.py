import re
import sys
import time
from dataclasses import dataclass

from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController


try:
    import win32api
    import win32con
    import win32gui
except ImportError:
    win32api = None
    win32con = None
    win32gui = None


FOREGROUND_MODE = "foreground"
BACKGROUND_MODE = "background"


class BackgroundInputError(RuntimeError):
    pass


@dataclass(frozen=True)
class WindowTarget:
    hwnd: int
    title: str
    class_name: str = ""

    @property
    def display_name(self):
        class_suffix = f" [{self.class_name}]" if self.class_name else ""
        return f"{self.title}{class_suffix} - {self.hwnd}"


def is_background_input_supported():
    return sys.platform == "win32" and win32api is not None and win32con is not None and win32gui is not None


def enumerate_windows(win32gui_module=None):
    gui = win32gui_module or win32gui
    if gui is None or (win32gui_module is None and sys.platform != "win32"):
        return []

    windows = []

    def callback(hwnd, _):
        if not gui.IsWindowVisible(hwnd):
            return

        title = gui.GetWindowText(hwnd).strip()
        if not title:
            return

        try:
            class_name = gui.GetClassName(hwnd)
        except Exception:
            class_name = ""

        windows.append(WindowTarget(hwnd=hwnd, title=title, class_name=class_name))

    gui.EnumWindows(callback, None)
    return windows


def find_minecraft_window(windows):
    matchers = [
        lambda title: "minecraft" in title.lower(),
        lambda title: "lunar" in title.lower(),
        lambda title: re.search(r"\b\d+\.\d+\.\d+\b", title) is not None,
    ]

    for matcher in matchers:
        for window in windows:
            if matcher(window.title):
                return window
    return windows[0] if windows else None


class PynputInputBackend:
    mode = FOREGROUND_MODE
    supports_text = True

    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def press_mouse(self, button):
        self.mouse.press(self._mouse_button(button))

    def release_mouse(self, button):
        self.mouse.release(self._mouse_button(button))

    def click_mouse(self, button):
        self.mouse.click(self._mouse_button(button))

    def move_mouse(self, x, y):
        self.mouse.position = (x, y)

    def press_key(self, key):
        self.keyboard.press(self._keyboard_key(key))

    def release_key(self, key):
        self.keyboard.release(self._keyboard_key(key))

    def tap_key(self, key):
        self.press_key(key)
        self.release_key(key)

    def type_text(self, text):
        self.keyboard.type(text)

    def release_all(self):
        self.release_mouse("left")
        self.release_mouse("right")
        for key in ("a", "d", "w", "s"):
            self.release_key(key)

    def _mouse_button(self, button):
        return {
            "left": Button.left,
            "right": Button.right,
        }[button]

    def _keyboard_key(self, key):
        if key == "enter":
            return Key.enter
        return key


class Win32WindowInputBackend:
    mode = BACKGROUND_MODE
    supports_text = True

    def __init__(self, target, win32api_module=None, win32con_module=None, win32gui_module=None):
        self.target = target
        self.hwnd = target.hwnd if isinstance(target, WindowTarget) else int(target)
        self.win32api = win32api_module or win32api
        self.win32con = win32con_module or win32con
        self.win32gui = win32gui_module or win32gui
        self._pressed_mouse_buttons = set()
        self._pressed_keys = set()

        if self.win32api is None or self.win32con is None or self.win32gui is None:
            raise BackgroundInputError("pywin32 jest niedostępne.")

        if hasattr(self.win32gui, "IsWindow") and not self.win32gui.IsWindow(self.hwnd):
            raise BackgroundInputError("Wybrane okno już nie istnieje.")

    def probe(self):
        try:
            self._post(self.win32con.WM_NULL, 0, 0)
            self._post_key("f24", key_down=True)
            self._post_key("f24", key_down=False)
            self._post_mouse_move()
            self._post(self.win32con.WM_CHAR, 0, 1)
        except Exception as exc:
            raise BackgroundInputError(f"Test wejścia w tle nie powiódł się: {exc}") from exc

    def press_mouse(self, button):
        message, state = self._mouse_messages(button, key_down=True)
        self._post_mouse(message, state)
        self._pressed_mouse_buttons.add(button)

    def release_mouse(self, button):
        message, state = self._mouse_messages(button, key_down=False)
        self._post_mouse(message, state)
        self._pressed_mouse_buttons.discard(button)

    def click_mouse(self, button):
        self.press_mouse(button)
        time.sleep(0.02)
        self.release_mouse(button)

    def move_mouse(self, x, y):
        self._post_mouse_move(x, y)

    def press_key(self, key):
        self._post_key(key, key_down=True)
        self._pressed_keys.add(key)

    def release_key(self, key):
        self._post_key(key, key_down=False)
        self._pressed_keys.discard(key)

    def tap_key(self, key):
        self.press_key(key)
        time.sleep(0.02)
        self.release_key(key)

    def type_text(self, text):
        for char in text:
            self._post(self.win32con.WM_CHAR, ord(char), 1)
            time.sleep(0.02)

    def release_all(self):
        for button in list(self._pressed_mouse_buttons) or ["left", "right"]:
            try:
                self.release_mouse(button)
            except BackgroundInputError:
                pass

        for key in list(self._pressed_keys) or ["a", "d", "w", "s"]:
            try:
                self.release_key(key)
            except BackgroundInputError:
                pass

    def _post(self, message, wparam, lparam):
        result = self.win32api.PostMessage(self.hwnd, message, wparam, lparam)
        if result == 0:
            raise BackgroundInputError("Windows odrzucił wysłaną wiadomość.")

    def _post_key(self, key, key_down):
        vk = self._virtual_key(key)
        scan_code = self.win32api.MapVirtualKey(vk, 0)
        message = self.win32con.WM_KEYDOWN if key_down else self.win32con.WM_KEYUP
        lparam = 1 | (scan_code << 16)
        if not key_down:
            lparam |= 1 << 30
            lparam |= 1 << 31
        self._post(message, vk, lparam)

    def _virtual_key(self, key):
        special_keys = {
            "enter": 0x0D,
            "f24": 0x87,
        }
        if key in special_keys:
            return special_keys[key]

        if len(key) != 1:
            raise BackgroundInputError(f"Nieobsługiwany klawisz dla trybu w tle: {key}")

        result = self.win32api.VkKeyScan(key)
        if result == -1:
            raise BackgroundInputError(f"Nieobsługiwany klawisz dla trybu w tle: {key}")

        return result & 0xFF

    def _mouse_messages(self, button, key_down):
        if button == "left":
            return (
                self.win32con.WM_LBUTTONDOWN if key_down else self.win32con.WM_LBUTTONUP,
                self.win32con.MK_LBUTTON if key_down else 0,
            )
        if button == "right":
            return (
                self.win32con.WM_RBUTTONDOWN if key_down else self.win32con.WM_RBUTTONUP,
                self.win32con.MK_RBUTTON if key_down else 0,
            )
        raise BackgroundInputError(f"Nieobsługiwany przycisk myszy dla trybu w tle: {button}")

    def _post_mouse(self, message, state):
        x, y = self._client_center()
        self._post(message, state, self._make_lparam(x, y))

    def _post_mouse_move(self, x=None, y=None):
        if x is None or y is None:
            x, y = self._client_center()
        self._post(self.win32con.WM_MOUSEMOVE, 0, self._make_lparam(x, y))

    def _client_center(self):
        left, top, right, bottom = self.win32gui.GetClientRect(self.hwnd)
        return max(0, (right - left) // 2), max(0, (bottom - top) // 2)

    def _make_lparam(self, x, y):
        if hasattr(self.win32api, "MAKELONG"):
            return self.win32api.MAKELONG(x, y)
        return (y << 16) | (x & 0xFFFF)
