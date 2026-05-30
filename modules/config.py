import configparser

CONFIG_PATH = "config.ini"


def _split_csv(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def reload():
    global file
    global version, horizontal_stones, vertical_stones, pickaxe, food
    global drop_slots, activity_rounds_config, activity_commands
    global cobblex_rounds_config, cobblex_commands, drop_rounds_config
    global eat_rounds_config, commands_delay_in_seconds, fast_pickaxe, slots

    file = configparser.ConfigParser()
    file.read(CONFIG_PATH)

    version = file["Version"]["version"]
    horizontal_stones = int(file["Config"]["horizontal_stones"])
    vertical_stones = int(file["Config"]["vertical_stones"])
    pickaxe = int(file["Config"]["pickaxe"])
    food = int(file["Config"]["food"])
    drop_slots = _split_csv(file["Config"]["drop_slots"])
    activity_rounds_config = int(file["Config"]["activity_rounds"])
    activity_commands = _split_csv(file["Config"]["activity_commands"])
    cobblex_rounds_config = int(file["Config"]["cobblex_rounds"])
    cobblex_commands = _split_csv(file["Config"]["cobblex_commands"])
    drop_rounds_config = int(file["Config"]["drop_rounds"])
    eat_rounds_config = int(file["Config"]["eat_rounds"])
    commands_delay_in_seconds = float(file["Config"]["commands_delay_in_seconds"])
    fast_pickaxe = file["Config"]["fast_pickaxe"].lower() == "true"
    slots = {
        "first_row_x": int(file["Slots"]["first_row_x"]),
        "first_row_y": int(file["Slots"]["first_row_y"]),
        "drop_x": int(file["Slots"]["drop_x"]),
        "drop_y": int(file["Slots"]["drop_y"]),
        "difference": int(file["Slots"]["difference"]),
    }


reload()
