import tempfile
import unittest
from pathlib import Path

import modules.config as config


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.original_config_path = config.CONFIG_PATH
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        config.CONFIG_PATH = self.root / "local-data" / "config.ini"

    def tearDown(self):
        self.temp_dir.cleanup()
        config.CONFIG_PATH = self.original_config_path
        config._apply_values(config._parser_from_text(config.DEFAULT_CONFIG))

    def test_creates_config_in_local_data_from_defaults(self):
        config.reload()

        self.assertTrue(config.CONFIG_PATH.exists())
        self.assertEqual(config.version, "0.7.0 BETA")
        self.assertEqual(config.horizontal_stones, 7)
        self.assertTrue(config.enable_eating)
        self.assertTrue(config.enable_dropping_items)
        self.assertTrue(config.enable_activity_commands)
        self.assertTrue(config.enable_cobblex)
        self.assertNotIn("[Version]", config.CONFIG_PATH.read_text(encoding="utf-8"))

    def test_save_config_text_validates_and_applies_values(self):
        updated_config = config.DEFAULT_CONFIG.replace("horizontal_stones = 7", "horizontal_stones = 11")

        config.save_config_text(updated_config)

        self.assertEqual(config.horizontal_stones, 11)
        self.assertIn("horizontal_stones = 11", config.CONFIG_PATH.read_text(encoding="utf-8"))

    def test_missing_feature_toggles_default_to_enabled(self):
        old_config = "\n".join(
            line
            for line in config.DEFAULT_CONFIG.splitlines()
            if not line.startswith("enable_")
        )

        config.save_config_text(old_config)

        self.assertTrue(config.enable_eating)
        self.assertTrue(config.enable_dropping_items)
        self.assertTrue(config.enable_activity_commands)
        self.assertTrue(config.enable_cobblex)

    def test_save_config_values_validates_and_applies_values(self):
        values = {
            "horizontal_stones": "8",
            "vertical_stones": "2",
            "pickaxe": "1",
            "eat_rounds": "20",
            "food": "5",
            "drop_rounds": "2",
            "drop_slots": "1, 2,3",
            "activity_rounds": "2",
            "activity_commands": "repair all, craftuj-wszystko",
            "cobblex_rounds": "3",
            "cobblex_commands": "cx",
            "commands_delay_in_seconds": "0,5",
            "fast_pickaxe": True,
            "enable_eating": False,
            "enable_dropping_items": True,
            "enable_activity_commands": False,
            "enable_cobblex": True,
            "first_row_x": "815",
            "first_row_y": "545",
            "drop_x": "371",
            "drop_y": "291",
            "difference": "36",
        }

        config.save_config_values(values)

        self.assertEqual(config.version, "0.7.0 BETA")
        self.assertEqual(config.horizontal_stones, 8)
        self.assertEqual(config.commands_delay_in_seconds, 0.5)
        self.assertEqual(config.drop_slots, ["1", "2", "3"])
        self.assertFalse(config.enable_eating)
        self.assertTrue(config.enable_dropping_items)
        self.assertFalse(config.enable_activity_commands)
        self.assertTrue(config.enable_cobblex)

    def test_save_config_values_rejects_invalid_ui_values(self):
        values = {
            "horizontal_stones": "8",
            "vertical_stones": "2",
            "pickaxe": "10",
            "eat_rounds": "20",
            "food": "5",
            "drop_rounds": "2",
            "drop_slots": "1",
            "activity_rounds": "2",
            "activity_commands": "repair all",
            "cobblex_rounds": "3",
            "cobblex_commands": "cx",
            "commands_delay_in_seconds": "1",
            "fast_pickaxe": True,
            "enable_eating": True,
            "enable_dropping_items": True,
            "enable_activity_commands": True,
            "enable_cobblex": True,
            "first_row_x": "815",
            "first_row_y": "545",
            "drop_x": "371",
            "drop_y": "291",
            "difference": "36",
        }

        with self.assertRaises(ValueError):
            config.save_config_values(values)

    def test_save_config_text_rejects_incomplete_config(self):
        with self.assertRaises(KeyError):
            config.save_config_text("[Config]\nhorizontal_stones = 3\n")

        self.assertFalse(config.CONFIG_PATH.exists())


if __name__ == "__main__":
    unittest.main()
