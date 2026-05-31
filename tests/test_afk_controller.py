import time
import unittest
from unittest.mock import patch

from modules.input_backends import FOREGROUND_MODE
from modules.afk_controller import AfkController


class FakeInputBackend:
    mode = FOREGROUND_MODE

    def __init__(self):
        self.events = []

    def press_mouse(self, button):
        self.events.append(("press_mouse", button))

    def release_mouse(self, button):
        self.events.append(("release_mouse", button))

    def release_all(self):
        self.events.append(("release_all", None))


class AfkControllerTests(unittest.TestCase):
    def test_fishing_holds_right_mouse_until_stopped(self):
        logs = []
        with patch("modules.afk_controller.PynputInputBackend", FakeInputBackend):
            controller = AfkController(log=logs.append)

        controller.start_fishing()
        self._wait_until(lambda: ("press_mouse", "right") in controller.foreground_backend.events)

        controller.stop()

        self.assertIn(("press_mouse", "right"), controller.foreground_backend.events)
        self.assertNotIn(("press_mouse", "left"), controller.foreground_backend.events)
        self.assertFalse(controller.is_running())

    def _wait_until(self, condition):
        deadline = time.time() + 1
        while time.time() < deadline:
            if condition():
                return
            time.sleep(0.01)
        self.fail("condition was not met before timeout")


if __name__ == "__main__":
    unittest.main()
