import unittest

from modules.input_backends import Win32WindowInputBackend
from modules.input_backends import WindowTarget
from modules.input_backends import enumerate_windows
from modules.input_backends import find_minecraft_window


class FakeWin32Con:
    WM_NULL = 0x0000
    WM_KEYDOWN = 0x0100
    WM_KEYUP = 0x0101
    WM_CHAR = 0x0102
    WM_MOUSEMOVE = 0x0200
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    WM_RBUTTONDOWN = 0x0204
    WM_RBUTTONUP = 0x0205
    MK_LBUTTON = 0x0001
    MK_RBUTTON = 0x0002


class FakeWin32Api:
    def __init__(self):
        self.messages = []

    def PostMessage(self, hwnd, message, wparam, lparam):
        self.messages.append((hwnd, message, wparam, lparam))
        return 1

    def MapVirtualKey(self, vk, map_type):
        return vk

    def VkKeyScan(self, key):
        if key == "/":
            return 0xBF
        return ord(key.upper())

    def MAKELONG(self, x, y):
        return (y << 16) | (x & 0xFFFF)


class FakeWin32Gui:
    windows = {
        1: {"visible": True, "title": "Minecraft 1.20.1", "class": "GLFW30", "rect": (0, 0, 1280, 720)},
        2: {"visible": True, "title": "Notepad", "class": "Notepad", "rect": (0, 0, 800, 600)},
        3: {"visible": False, "title": "Hidden", "class": "Hidden", "rect": (0, 0, 1, 1)},
    }

    def EnumWindows(self, callback, extra):
        for hwnd in self.windows:
            callback(hwnd, extra)

    def IsWindowVisible(self, hwnd):
        return self.windows[hwnd]["visible"]

    def GetWindowText(self, hwnd):
        return self.windows[hwnd]["title"]

    def GetClassName(self, hwnd):
        return self.windows[hwnd]["class"]

    def IsWindow(self, hwnd):
        return hwnd in self.windows

    def GetClientRect(self, hwnd):
        return self.windows[hwnd]["rect"]


class InputBackendTests(unittest.TestCase):
    def test_enumerates_visible_titled_windows_and_selects_minecraft(self):
        windows = enumerate_windows(win32gui_module=FakeWin32Gui())

        self.assertEqual([window.title for window in windows], ["Minecraft 1.20.1", "Notepad"])
        self.assertEqual(find_minecraft_window(windows).title, "Minecraft 1.20.1")

    def test_selects_lunar_before_version_title(self):
        windows = [
            WindowTarget(hwnd=1, title="Notepad"),
            WindowTarget(hwnd=2, title="Client 1.21.11"),
            WindowTarget(hwnd=3, title="Lunar Client"),
        ]

        self.assertEqual(find_minecraft_window(windows).title, "Lunar Client")

    def test_selects_minecraft_before_lunar_title(self):
        windows = [
            WindowTarget(hwnd=1, title="Lunar Client"),
            WindowTarget(hwnd=2, title="Minecraft 1.21.11"),
        ]

        self.assertEqual(find_minecraft_window(windows).title, "Minecraft 1.21.11")

    def test_selects_version_title_when_minecraft_and_lunar_are_missing(self):
        windows = [
            WindowTarget(hwnd=1, title="Notepad"),
            WindowTarget(hwnd=2, title="Game 1.21.11"),
        ]

        self.assertEqual(find_minecraft_window(windows).title, "Game 1.21.11")

    def test_win32_backend_posts_probe_and_input_messages(self):
        api = FakeWin32Api()
        con = FakeWin32Con()
        backend = Win32WindowInputBackend(
            WindowTarget(hwnd=1, title="Minecraft 1.20.1"),
            win32api_module=api,
            win32con_module=con,
            win32gui_module=FakeWin32Gui(),
        )

        backend.probe()
        backend.press_key("d")
        backend.release_key("d")
        backend.type_text("/cx")
        backend.press_mouse("left")
        backend.release_mouse("left")
        backend.press_mouse("right")
        backend.release_mouse("right")

        posted_messages = [message for _, message, _, _ in api.messages]
        self.assertIn(con.WM_NULL, posted_messages)
        self.assertIn(con.WM_KEYDOWN, posted_messages)
        self.assertIn(con.WM_KEYUP, posted_messages)
        self.assertIn(con.WM_CHAR, posted_messages)
        self.assertIn(con.WM_MOUSEMOVE, posted_messages)
        self.assertIn(con.WM_LBUTTONDOWN, posted_messages)
        self.assertIn(con.WM_LBUTTONUP, posted_messages)
        self.assertIn(con.WM_RBUTTONDOWN, posted_messages)
        self.assertIn(con.WM_RBUTTONUP, posted_messages)


if __name__ == "__main__":
    unittest.main()
