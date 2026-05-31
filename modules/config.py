import configparser
import os
import sys
from pathlib import Path

APP_NAME = "MineAFK"
CONFIG_FILENAME = "config.ini"
VERSION_FILENAME = "version.txt"
DEFAULT_VERSION = "0.7.0 BETA"

DEFAULT_CONFIG = """[Config]
horizontal_stones = 7
vertical_stones = 2
pickaxe = 1
eat_rounds = 20
food = 5
drop_rounds = 2
drop_slots = 1
activity_rounds = 2
activity_commands = repair all,craftuj-wszystko
cobblex_rounds = 3
cobblex_commands = cx
commands_delay_in_seconds = 1
fast_pickaxe = true
enable_eating = true
enable_dropping_items = true
enable_activity_commands = true
enable_cobblex = true

[Slots]
first_row_x = 815
first_row_y = 545
drop_x = 371
drop_y = 291
difference = 36
"""


def _split_csv(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def _resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / filename
    return Path(__file__).resolve().parent.parent / filename


def _read_app_version():
    try:
        return _resource_path(VERSION_FILENAME).read_text(encoding="utf-8").strip()
    except OSError:
        return DEFAULT_VERSION


def _format_csv(values):
    return ",".join(str(value).strip() for value in values if str(value).strip())


def _parse_int(values, key, label, minimum=None, maximum=None):
    raw_value = str(values.get(key, "")).strip()
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{label}: wpisz liczbę całkowitą.") from exc

    if minimum is not None and value < minimum:
        raise ValueError(f"{label}: minimalna wartość to {minimum}.")
    if maximum is not None and value > maximum:
        raise ValueError(f"{label}: maksymalna wartość to {maximum}.")
    return value


def _parse_float(values, key, label, minimum=None):
    raw_value = str(values.get(key, "")).strip().replace(",", ".")
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"{label}: wpisz liczbę.") from exc

    if minimum is not None and value < minimum:
        raise ValueError(f"{label}: minimalna wartość to {minimum}.")
    return value


def _parse_bool(values, key, label):
    value = values.get(key, "")
    if isinstance(value, bool):
        return value

    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "tak"}:
        return True
    if normalized in {"false", "0", "no", "nie"}:
        return False
    raise ValueError(f"{label}: wybierz true albo false.")


def _parse_slot_list(values, key, label):
    slots = []
    for item in _split_csv(str(values.get(key, ""))):
        try:
            slot = int(item)
        except ValueError as exc:
            raise ValueError(f"{label}: każdy slot musi być liczbą całkowitą.") from exc
        if slot < 1 or slot > 36:
            raise ValueError(f"{label}: sloty muszą być w zakresie 1-36.")
        slots.append(slot)
    return slots


def _default_config_dir():
    configured_dir = os.environ.get("MINEAFK_CONFIG_DIR")
    if configured_dir:
        return Path(configured_dir).expanduser()

    configured_path = os.environ.get("MINEAFK_CONFIG_PATH")
    if configured_path:
        return Path(configured_path).expanduser().parent

    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / APP_NAME
        return Path.home() / "AppData" / "Local" / APP_NAME

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_NAME

    config_home = os.environ.get("XDG_CONFIG_HOME")
    if config_home:
        return Path(config_home) / APP_NAME
    return Path.home() / ".config" / APP_NAME


def _config_path():
    configured_path = os.environ.get("MINEAFK_CONFIG_PATH")
    if configured_path:
        return Path(configured_path).expanduser()
    return _default_config_dir() / CONFIG_FILENAME


CONFIG_PATH = _config_path()
version = _read_app_version()


def ensure_config_file():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if CONFIG_PATH.exists():
        return CONFIG_PATH

    CONFIG_PATH.write_text(DEFAULT_CONFIG, encoding="utf-8")
    return CONFIG_PATH


def _parser_from_text(text):
    parser = configparser.ConfigParser()
    parser.read_string(text)
    return parser


def _load_values(parser):
    values = {
        "horizontal_stones": int(parser["Config"]["horizontal_stones"]),
        "vertical_stones": int(parser["Config"]["vertical_stones"]),
        "pickaxe": int(parser["Config"]["pickaxe"]),
        "food": int(parser["Config"]["food"]),
        "drop_slots": _split_csv(parser["Config"]["drop_slots"]),
        "activity_rounds_config": int(parser["Config"]["activity_rounds"]),
        "activity_commands": _split_csv(parser["Config"]["activity_commands"]),
        "cobblex_rounds_config": int(parser["Config"]["cobblex_rounds"]),
        "cobblex_commands": _split_csv(parser["Config"]["cobblex_commands"]),
        "drop_rounds_config": int(parser["Config"]["drop_rounds"]),
        "eat_rounds_config": int(parser["Config"]["eat_rounds"]),
        "commands_delay_in_seconds": float(parser["Config"]["commands_delay_in_seconds"]),
        "fast_pickaxe": parser["Config"]["fast_pickaxe"].lower() == "true",
        "enable_eating": _parse_bool(parser["Config"], "enable_eating", "Jedzenie") if "enable_eating" in parser["Config"] else True,
        "enable_dropping_items": _parse_bool(parser["Config"], "enable_dropping_items", "Wyrzucanie itemów") if "enable_dropping_items" in parser["Config"] else True,
        "enable_activity_commands": _parse_bool(parser["Config"], "enable_activity_commands", "Komendy aktywności") if "enable_activity_commands" in parser["Config"] else True,
        "enable_cobblex": _parse_bool(parser["Config"], "enable_cobblex", "Cobblex") if "enable_cobblex" in parser["Config"] else True,
        "slots": {
            "first_row_x": int(parser["Slots"]["first_row_x"]),
            "first_row_y": int(parser["Slots"]["first_row_y"]),
            "drop_x": int(parser["Slots"]["drop_x"]),
            "drop_y": int(parser["Slots"]["drop_y"]),
            "difference": int(parser["Slots"]["difference"]),
        },
    }
    return values


def _apply_values(parser):
    global file
    global horizontal_stones, vertical_stones, pickaxe, food
    global drop_slots, activity_rounds_config, activity_commands
    global cobblex_rounds_config, cobblex_commands, drop_rounds_config
    global eat_rounds_config, commands_delay_in_seconds, fast_pickaxe, slots
    global enable_eating, enable_dropping_items, enable_activity_commands, enable_cobblex

    values = _load_values(parser)
    file = parser
    horizontal_stones = values["horizontal_stones"]
    vertical_stones = values["vertical_stones"]
    pickaxe = values["pickaxe"]
    food = values["food"]
    drop_slots = values["drop_slots"]
    activity_rounds_config = values["activity_rounds_config"]
    activity_commands = values["activity_commands"]
    cobblex_rounds_config = values["cobblex_rounds_config"]
    cobblex_commands = values["cobblex_commands"]
    drop_rounds_config = values["drop_rounds_config"]
    eat_rounds_config = values["eat_rounds_config"]
    commands_delay_in_seconds = values["commands_delay_in_seconds"]
    fast_pickaxe = values["fast_pickaxe"]
    enable_eating = values["enable_eating"]
    enable_dropping_items = values["enable_dropping_items"]
    enable_activity_commands = values["enable_activity_commands"]
    enable_cobblex = values["enable_cobblex"]
    slots = values["slots"]


def validate_config_text(text):
    parser = _parser_from_text(text)
    _load_values(parser)
    return parser


def build_config_text(values):
    horizontal_stones_value = _parse_int(values, "horizontal_stones", "Stoniarki w szerokości", minimum=1)
    vertical_stones_value = _parse_int(values, "vertical_stones", "Stoniarki przód/tył", minimum=0)
    pickaxe_value = _parse_int(values, "pickaxe", "Slot kilofa", minimum=1, maximum=9)
    eat_rounds_value = _parse_int(values, "eat_rounds", "Rundy jedzenia", minimum=1)
    food_value = _parse_int(values, "food", "Slot jedzenia", minimum=0, maximum=9)
    drop_rounds_value = _parse_int(values, "drop_rounds", "Rundy wyrzucania", minimum=1)
    drop_slots_value = _parse_slot_list(values, "drop_slots", "Sloty do wyrzucenia")
    activity_rounds_value = _parse_int(values, "activity_rounds", "Rundy aktywności", minimum=1)
    activity_commands_value = _format_csv(_split_csv(str(values.get("activity_commands", ""))))
    cobblex_rounds_value = _parse_int(values, "cobblex_rounds", "Rundy cobblex", minimum=1)
    cobblex_commands_value = _format_csv(_split_csv(str(values.get("cobblex_commands", ""))))
    commands_delay_value = _parse_float(values, "commands_delay_in_seconds", "Odstęp między komendami", minimum=0)
    fast_pickaxe_value = _parse_bool(values, "fast_pickaxe", "Szybki kilof")
    enable_eating_value = _parse_bool(values, "enable_eating", "Jedzenie")
    enable_dropping_items_value = _parse_bool(values, "enable_dropping_items", "Wyrzucanie itemów")
    enable_activity_commands_value = _parse_bool(values, "enable_activity_commands", "Komendy aktywności")
    enable_cobblex_value = _parse_bool(values, "enable_cobblex", "Cobblex")
    first_row_x_value = _parse_int(values, "first_row_x", "Slot 1 X")
    first_row_y_value = _parse_int(values, "first_row_y", "Slot 1 Y")
    drop_x_value = _parse_int(values, "drop_x", "Miejsce wyrzucania X")
    drop_y_value = _parse_int(values, "drop_y", "Miejsce wyrzucania Y")
    difference_value = _parse_int(values, "difference", "Odstęp slotów", minimum=1)

    return (
        "[Config]\n"
        f"horizontal_stones = {horizontal_stones_value}\n"
        f"vertical_stones = {vertical_stones_value}\n"
        f"pickaxe = {pickaxe_value}\n"
        f"eat_rounds = {eat_rounds_value}\n"
        f"food = {food_value}\n"
        f"drop_rounds = {drop_rounds_value}\n"
        f"drop_slots = {_format_csv(drop_slots_value)}\n"
        f"activity_rounds = {activity_rounds_value}\n"
        f"activity_commands = {activity_commands_value}\n"
        f"cobblex_rounds = {cobblex_rounds_value}\n"
        f"cobblex_commands = {cobblex_commands_value}\n"
        f"commands_delay_in_seconds = {commands_delay_value:g}\n"
        f"fast_pickaxe = {str(fast_pickaxe_value).lower()}\n"
        f"enable_eating = {str(enable_eating_value).lower()}\n"
        f"enable_dropping_items = {str(enable_dropping_items_value).lower()}\n"
        f"enable_activity_commands = {str(enable_activity_commands_value).lower()}\n"
        f"enable_cobblex = {str(enable_cobblex_value).lower()}\n"
        "\n"
        "[Slots]\n"
        f"first_row_x = {first_row_x_value}\n"
        f"first_row_y = {first_row_y_value}\n"
        f"drop_x = {drop_x_value}\n"
        f"drop_y = {drop_y_value}\n"
        f"difference = {difference_value}\n"
    )


def read_config_text():
    ensure_config_file()
    return CONFIG_PATH.read_text(encoding="utf-8")


def save_config_text(text):
    parser = validate_config_text(text)
    ensure_config_file()
    CONFIG_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")
    _apply_values(parser)


def save_config_values(values):
    save_config_text(build_config_text(values))


def update_slots(slot_values):
    ensure_config_file()
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")
    if "Slots" not in parser:
        parser["Slots"] = {}

    for key, value in slot_values.items():
        parser["Slots"][key] = str(value)

    _load_values(parser)
    with CONFIG_PATH.open("w", encoding="utf-8") as config_file:
        parser.write(config_file)

    _apply_values(parser)


def reload():
    ensure_config_file()
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")
    _apply_values(parser)


_apply_values(_parser_from_text(DEFAULT_CONFIG))
